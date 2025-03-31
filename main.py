import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from face_detection import detect_faces
from camera import open_camera, close_camera
import time

# Initialize Tkinter window
root = tk.Tk()
root.title("Face Recognition App")
root.geometry("1024x720")  # Fixed window size
root.configure(bg="black")  # Background color

# Header Label for a fancier look
header_label = Label(root, text="Face Recognition App", font=("Helvetica", 24, "bold"),
                     bg="black", fg="white")
header_label.pack(side=tk.TOP, fill=tk.X, pady=10)

# OpenCV Video Capture
cap = open_camera()
if not cap.isOpened():
    print("Error: Could not open video device")

# Tkinter Label to show video feed with a raised border for a sleek look
video_label = Label(root, bg="black", bd=2, relief="raised")
video_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Status Bar for Frame Rate and Detection Count
status_label = Label(root, text="FPS: 0 | Faces Detected: 0", font=("Helvetica", 14),
                     bg="black", fg="white")
status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

prev_time = time.time()

def show_frame():
    """Captures video frames, detects faces, resizes, updates the GUI, and shows FPS."""
    global prev_time
    ret, frame = cap.read()
    if ret:
        faces = detect_faces(frame)
        num_faces = len(faces)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
        # Resize frame to fit window
        frame = cv2.resize(frame, (1024, 720))
        
        # Convert frame from BGR to RGB for Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Update the label with new frame
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
        # Calculate FPS
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time))
        prev_time = curr_time
        
        # Update status bar with FPS and face count
        status_label.config(text=f"FPS: {fps} | Faces Detected: {num_faces}")
        
        video_label.after(10, show_frame)
    else:
        print("Failed to capture frame")
        video_label.after(1000, show_frame)  # Retry after a delay if no frame

show_frame()  # Start the video loop

# Close webcam on window close
def on_closing():
    """Releases the webcam and closes the application."""
    close_camera(cap)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
