from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from app.state.app_state import AppState

class CalibrationScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.addWidget(QLabel("CALIBRATION SCREEN"))

        btn = QPushButton("Calibration Done")
        btn.clicked.connect(self.go_next)

        layout.addWidget(btn)
        self.setLayout(layout)

    def go_next(self):
        self.main_window.switch_state(AppState.HOME)
