from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action

class MicButton(FocusableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("🎤 START RECORDING", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 22px;")

        self.resize(360, 360)
        self.recording = False

    def set_recording(self, recording: bool):
        self.recording = recording
        if recording:
            self.label.setText("⏹ STOP RECORDING")
        else:
            self.label.setText("🎤 START RECORDING")

    def select(self):
        return Action.VOICE_TOGGLE
