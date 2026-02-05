import cv2
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

from core.vision.face_auth import FaceAuthenticator


class LoginScreen(QWidget):
    login_success = pyqtSignal(str)
    new_user_detected = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Face Login")

        self.video_label = QLabel()
        self.scan_button = QPushButton("Scan Face")

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.scan_button)
        self.setLayout(layout)

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.authenticator = FaceAuthenticator()
        self.current_frame = None

        self.scan_button.clicked.connect(self.scan_face)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        self.current_frame = frame

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        qt_image = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def scan_face(self):
        user_id = self.authenticator.authenticate(self.current_frame)

        if user_id:
            self.login_success.emit(user_id)
        else:
            self.new_user_detected.emit()

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()
