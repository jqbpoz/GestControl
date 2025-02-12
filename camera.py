import cv2
from PyQt6.QtCore import QThread, pyqtSignal

class CameraThread(QThread):
    """Thread to handle camera loading in the background."""
    camera_started = pyqtSignal()

    def run(self):
        """Start the camera feed in the background and signal when it's ready."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.camera_started.emit()
            return
        self.camera_started.emit()
