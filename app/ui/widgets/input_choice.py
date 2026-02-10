from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action


class ChoiceButton(FocusableWidget):
    def __init__(self, label: str, action: Action, parent=None):
        super().__init__(parent)
        self.action = action

        self.text = QLabel(label, self)
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text.setStyleSheet("font-size: 18px;")

        self.resize(220, 100)

    def select(self):
        return self.action

class InputChoiceOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.voice_btn = ChoiceButton("VOICE INPUT", Action.VOICE_INPUT, self)
        self.keyboard_btn = ChoiceButton("KEYBOARD INPUT", Action.OPEN_TYPING_KEYBOARD, self)

        # manual positioning (IMPORTANT)
        self.voice_btn.move(0, 0)
        self.keyboard_btn.move(260, 0)

        self.voice_btn.resize(220, 100)
        self.keyboard_btn.resize(220, 100)

        self.focusables = [
            self.voice_btn,
            self.keyboard_btn
        ]
