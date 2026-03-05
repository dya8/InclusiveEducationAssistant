from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action


class SaveButton(FocusableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(220, 100)

        self.label = QLabel("💾 SAVE NOTE", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size:20px;")
        self.label.setGeometry(0,0,220,100)

    def select(self):
        return Action.SAVE_NOTE