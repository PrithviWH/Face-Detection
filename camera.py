import cv2

def open_camera():
    """Opens the webcam and returns the video capture object."""
    return cv2.VideoCapture(0)

def close_camera(cap):
    """Releases the webcam."""
    cap.release()
    cv2.destroyAllWindows()
