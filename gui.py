import cv2
import numpy as np
import mediapipe as mp
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt
from camera import CameraThread
from control import set_volume, set_brightness
from utils import load_available_cameras


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

class HandVolumeControlApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Volume and Brightness Control")
        self.setGeometry(100, 100, 900, 700)


        self.layout = QHBoxLayout()


        self.video_layout = QVBoxLayout()

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("background-color: #2c3e50; color: white; font-size: 18px;")
        self.video_layout.addWidget(self.video_label)


        self.control_layout = QVBoxLayout()

        self.switch_button = QPushButton("Switch Mode", self)
        self.switch_button.clicked.connect(self.switch_mode)
        self.control_layout.addWidget(self.switch_button)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.control_layout.addWidget(self.pause_button)

        self.mode_label = QLabel("Mode: Volume", self)
        self.control_layout.addWidget(self.mode_label)
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.percentage_label = QLabel("0%", self)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.control_layout.addWidget(self.percentage_label)


        self.camera_selector = QComboBox(self)
        self.control_layout.addWidget(self.camera_selector)


        self.paused_label = QLabel("", self)
        self.paused_label.setStyleSheet("color: yellow; font-size: 18px;")
        self.control_layout.addWidget(self.paused_label)


        self.layout.addLayout(self.video_layout)
        self.layout.addLayout(self.control_layout)

        self.setLayout(self.layout)


        self.mode = "volume"
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.paused = False

        self.setStyleSheet("""
            QWidget {
                background-color: #34495e;
                color: white;
                font-size: 16px;
                font-style : "consolas";
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
                font-style : "consolas";
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QLabel {
                line-height:0;
                padding: 5px;
                font-size: 18px;
                border-radius: 5px;
                font-style : "consolas";
            }
        """)



        self.loading_label = QLabel("Starting Camera...", self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("color: white; font-size: 24px; background-color: #34495e;")
        self.video_layout.addWidget(self.loading_label)


        self.camera_thread = CameraThread()
        self.camera_thread.camera_started.connect(self.on_camera_started)
        self.camera_thread.start()

        self.mode_label.setFixedHeight(46)
        self.loading_label.setFixedHeight(46)
        self.percentage_label.setFixedHeight(46)

        self.layout.setContentsMargins(40, 40, 40, 40)
        self.video_layout.setAlignment(Qt.AlignmentFlag.AlignTop)



    def on_camera_started(self):
        self.loading_label.setText("Camera is ready.")
        self.load_cameras()
        self.change_camera()

    def load_cameras(self):
        cameras = load_available_cameras()
        for cam in cameras:
            self.camera_selector.addItem(f"Camera {cam}", cam)
        self.camera_selector.currentIndexChanged.connect(self.change_camera)

    def change_camera(self):
        if self.cap:
            self.cap.release()
        camera_index = self.camera_selector.currentData()
        self.cap = cv2.VideoCapture(camera_index)
        self.timer.start(30)

    def switch_mode(self):
        self.mode = "brightness" if self.mode == "volume" else "volume"
        self.mode_label.setText(f"Mode: {'Brightness' if self.mode == 'brightness' else 'Volume'}")

    def toggle_pause(self):
        if self.paused:
            self.paused = False
            self.pause_button.setText("Pause")
            self.paused_label.setText("")
        else:
            self.paused = True
            self.pause_button.setText("Resume")
            self.paused_label.setText("Value updates paused")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                h, w, _ = frame.shape
                x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
                x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

                distance = np.linalg.norm([x2 - x1, y2 - y1])
                value = np.interp(distance, [30, 300], [0, 100])

                if not self.paused:
                    if self.mode == "volume":
                        set_volume(value)
                    else:
                        set_brightness(value)

                    self.percentage_label.setText(f"{int(value)}%")

        qimg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg).scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        event.accept()

