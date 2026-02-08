from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from core.input.input_events import Action

class KeyboardIcon(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(0, 0)
        self.setText("⌨")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background:#333; color:white; border-radius:10px;")

    def set_focus(self, focused: bool):
        if focused:
            self.setStyleSheet("background:#00aa88; color:white; border-radius:10px;")
        else:
            self.setStyleSheet("background:#333; color:white; border-radius:10px;")

    def update_dwell(self, progress: float):
        pass  # optional

    def select(self):
        print("Keyboard icon selected")
        return Action.OPEN_KEYBOARD
