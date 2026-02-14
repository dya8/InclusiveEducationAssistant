from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action


class BackButton(FocusableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("⬅ BACK", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px;")

        self.resize(160, 80)

    def select(self):
        return Action.BACK
