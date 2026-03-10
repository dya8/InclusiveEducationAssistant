from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget


class CodingKeyButton(FocusableWidget):

    def __init__(self, text, action=None, value=None, parent=None):
        super().__init__(parent)

        self.action = action
        self.value = value

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setStyleSheet("""
            font-size:22px;
            color:white;
        """)

        self.setMinimumSize(120,70)

    def resizeEvent(self, event):
        self.label.resize(self.size())

    def select(self):
        print("BUTTON:", self.label.text(), self.action, self.value)

        if self.value is None:
            return self.action

        return (self.action, self.value)