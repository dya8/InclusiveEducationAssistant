from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from core.audio.stt import listen_once
from PyQt6.QtCore import QThread, pyqtSignal
from core.input.input_events import Action
from app.ui.widgets.input_choice import InputChoiceOverlay
from app.ui.widgets.focusable import FocusableWidget
from app.ui.widgets.typing_keyboard import TypingKeyboard
class NotesScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        title = QLabel("Take Notes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px;")

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.choice_overlay = InputChoiceOverlay(self)
        self.choice_overlay.hide()

        self.text_focus = NotesFocusArea(self.text_area, self)
        self.keyboard = TypingKeyboard(self)
        self.keyboard.hide()

        layout.addWidget(title)
        layout.addWidget(self.text_area)
        layout.addWidget(self.keyboard)

        self.setLayout(layout)
        self.text_focus.raise_()
        # ---------- CENTER INPUT CHOICE OVERLAY ----------
        overlay_width = 500
        overlay_height = 140

        self.choice_overlay.resize(overlay_width, overlay_height)

        parent_width = self.parent().width()
        parent_height = self.parent().height()

        x = (parent_width - overlay_width) // 2
        y = (parent_height - overlay_height) // 2

        self.choice_overlay.move(x, y)
        self.choice_overlay.raise_()

        self.typing_active = False
        self.voice_active = False
    def add_text(self, text: str):
        self.text_area.insertPlainText(text + " ")
    from app.ui.widgets.focusable import FocusableWidget
    def start_voice_input(self):
        if self.voice_active:
            return

        self.voice_active = True

        self.voice_worker = VoiceWorker()
        self.voice_worker.finished.connect(self.on_voice_result)
        self.voice_worker.start()
    def on_voice_result(self, text: str):
        self.add_text(text)
        self.voice_active = False


class NotesFocusArea(FocusableWidget):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.widget = widget
        self.setGeometry(widget.geometry())

    def select(self):
        return Action.SELECT

class VoiceWorker(QThread):
    finished = pyqtSignal(str)

    def run(self):
        text = listen_once()
        if text:
            self.finished.emit(text)
