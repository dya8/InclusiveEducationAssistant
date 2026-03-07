from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action


class DeleteButton(FocusableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(220, 70)

        self.label = QLabel("DELETE NOTE", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, 220, 70)

        self.setStyleSheet("""
            background:#8b0000;
            color:white;
            font-size:22px;
            border-radius:10px;
        """)

    def select(self):
        print("DELETE BUTTON SELECTED")
        return Action.DELETE_NOTE