import cv2

def load_available_cameras():
    """Detect and load available cameras on the system."""
    camera_list = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        camera_list.append(index)
        cap.release()
        index += 1
    return camera_list
