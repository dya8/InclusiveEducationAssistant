'''from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action


class GazeButton(FocusableWidget):

    def __init__(self, text, action=Action.NONE, value=None, parent=None):
        super().__init__(parent)

        self.action = action
        self.value = value

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setStyleSheet("""
            font-size: 24px;
            font-weight: 500;
            color: white;
        """)

        self.resize(200, 110)
        self.label.resize(self.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.label.resize(self.size())

    def select(self):
        print("BUTTON RETURNING:", self.action, self.value)   # DEBUG
        return self.action, self.value'''