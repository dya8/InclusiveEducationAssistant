from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel
)
from PyQt6.QtCore import Qt

from core.input.input_events import Action
from app.ui.widgets.input_choice import InputChoiceOverlay
from app.ui.widgets.focusable import FocusableWidget
from app.ui.widgets.typing_keyboard import TypingKeyboard
from core.audio.stt import VoiceWorker
from app.ui.widgets.mic_button import MicButton
from core.input.input_events import Action


class NotesScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------- LAYOUT ----------
        layout = QVBoxLayout()

        title = QLabel("Take Notes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px;")

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        layout.addWidget(title)
        layout.addWidget(self.text_area)

        # ---------- INPUT CHOICE ----------
        self.choice_overlay = InputChoiceOverlay(self)
        self.choice_overlay.hide()

        # ---------- KEYBOARD ----------
        self.keyboard = TypingKeyboard(self)
        self.keyboard.hide()
        layout.addWidget(self.keyboard)

        self.setLayout(layout)

        # ---------- FOCUS ----------
        self.text_focus = NotesFocusArea(self.text_area, self)
        self.text_focus.raise_()

        # ---------- CENTER INPUT CHOICE ----------
        overlay_width = 500
        overlay_height = 140
        self.choice_overlay.resize(overlay_width, overlay_height)

        pw = self.parent().width()
        ph = self.parent().height()
        self.choice_overlay.move(
            (pw - overlay_width) // 2,
            (ph - overlay_height) // 2
        )
        self.choice_overlay.raise_()

        # ---------- VOICE STATE ----------
        self.voice_active = False
        self.voice_worker = None

        # ---------- MIC INDICATOR ----------
        self.mic_button = MicButton(self)
        self.mic_button.move(
            (pw - 360) // 2,
            ph - 140
        )
        self.mic_button.hide()

        self.mic_label = QLabel("🎤 Recording...", self)
        self.mic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mic_label.setStyleSheet(
            "font-size: 28px; background: rgba(0,0,0,0.7); color: white; padding: 20px;"
        )
        self.mic_label.hide()

        self.mic_label.adjustSize()
        self.mic_label.move(
            (pw - self.mic_label.width()) // 2,
            ph - 200
        )
        self.mic_label.raise_()

        #====typing keyboard===
        self.keyboard = TypingKeyboard(self)
        self.keyboard.hide()
        layout.addWidget(self.keyboard)

        # ---------- FLAGS ----------
        self.typing_active = False

    # ==================================================
    # TEXT
    # ==================================================

    def add_text(self, text: str):
        if text.strip():
            self.text_area.insertPlainText(text + " ")

        # ==================================================
    # VOICE INPUT (BLINK TOGGLE)
    # ==================================================

    def toggle_voice_input(self):
        if self.voice_active:
            self.stop_voice_input()
        else:
            self.start_voice_input()

    def start_voice_input(self):
        if self.voice_active:
            return

        self.voice_active = True
        self.mic_label.show()
        self.mic_button.set_recording(True)

        self.voice_worker = VoiceWorker()
        self.voice_worker.finished.connect(self.on_voice_result)
        self.voice_worker.start()

    def stop_voice_input(self):
        if not self.voice_active:
            return

        #self.voice_active = False
        #self.mic_label.hide()
        #self.mic_button.set_recording(False)

        if self.voice_worker:
            self.voice_worker.stop()   # 🔑 REQUIRED

    def on_voice_result(self, text: str):
        self.voice_active = False
        self.mic_label.hide()
        self.mic_button.set_recording(False)

        if text and text.strip():
            self.add_text(text)
        # 🔑 CLEAN EXIT
        self.voice_worker = None

    def handle_keyboard_action(self, action, value):
        if action == Action.INSERT_CHAR:
            self.add_text(value)

        elif action == Action.SPACE:
            self.add_text(" ")

        elif action == Action.BACKSPACE:
            cursor = self.text_area.textCursor()
            cursor.deletePreviousChar()

        elif action == Action.DONE:
            self.keyboard.hide()
            self.typing_active = False



class NotesFocusArea(FocusableWidget):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.setGeometry(widget.geometry())

    def select(self):
        return Action.SELECT
