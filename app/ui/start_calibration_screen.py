from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from app.state.app_state import AppState


class StartCalibrationScreen(QWidget):
    start_clicked = pyqtSignal()
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # -------- Full Grey Background --------
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E2E;
            }
        """)

        # -------- Layout (IMPORTANT FIX) --------
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(50)

        # -------- Eye Logo --------
        self.logo = QLabel()
        pixmap = QPixmap("assets/images/eye.jpeg")
        self.logo.setPixmap(
            pixmap.scaled(350, 220,
                          Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -------- Start Button --------
        self.start_button = QPushButton("Start Calibration")
        self.start_button.setFixedSize(320, 60)

        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #89B4FA;
                color: #1E1E2E;
                font-size: 20px;
                font-weight: bold;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #B4BEFE;
            }
        """)

        self.start_button.clicked.connect(self.go_to_calibration)

        layout.addWidget(self.logo)
        layout.addWidget(self.start_button)

    def go_to_calibration(self):
        self.start_clicked.emit()