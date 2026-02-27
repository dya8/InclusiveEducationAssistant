from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor
from core.nlp.predictor import Predictor
from core.input.input_events import Action
from app.ui.widgets.input_choice import InputChoiceOverlay
from app.ui.widgets.focusable import FocusableWidget
from app.ui.widgets.typing_keyboard import TypingKeyboard
from core.audio.stt import VoiceWorker
from app.ui.widgets.mic_button import MicButton
from core.input.input_events import Action
from app.ui.widgets.back_button import BackButton
from core.nlp.tokenizer import extract_context_and_prefix
from app.ui.widgets.suggestion_bar import SuggestionBar

class NotesScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------- LAYOUT ----------
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 24, 60, 30)
        layout.setSpacing(15)
        # Header row
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)
        self.back_button = BackButton(self)
        title = QLabel("Take Notes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 34px;
            font-weight: 600;
            color: #222;
        """)
        header_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setMinimumHeight(220)
        self.text_area.setStyleSheet("""
            QTextEdit {
                font-size: 28px;
                padding: 20px;
                border: 2px solid #444;
                border-radius: 12px;
                color: white;
            }
        """)
        
        layout.addWidget(self.text_area,stretch=4)

        # ---------- INPUT CHOICE ----------
        self.choice_overlay = InputChoiceOverlay(self)
        self.choice_overlay.hide()
        self.suggestion_bar = SuggestionBar(self)
        layout.addWidget(self.suggestion_bar)
        self.suggestion_bar.suggestion_selected.connect(
            self.on_suggestion_selected
        )
        # ---------- KEYBOARD ----------
        #self.keyboard = TypingKeyboard(self)
        #self.keyboard.hide()
        #layout.addWidget(self.keyboard)
        self.text_buffer = ""
        self.predictor = Predictor("assets/models/ngram_model.pkl")

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
        self.keyboard.setMinimumHeight(650)
        self.keyboard.hide()
        layout.addWidget(self.keyboard, stretch=5)
        self.setLayout(layout)
        # ---------- FLAGS ----------
        self.typing_active = False

        #self.back_button = BackButton(self)
        #self.back_button.move(20, 20)
        #self.back_button.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        print("Keyboard height:", self.keyboard.height())
        # Center overlay
        overlay_width = 500
        overlay_height = 140
        self.choice_overlay.move(
            (self.width() - overlay_width) // 2,
            int(self.height() * 0.4)
        )

        # Back button stays top-left
        self.back_button.move(30, 20)
        # Optional: reposition mic button
        self.mic_button.move(
            (self.width() - 360) // 2,
            self.height() - 140
        )

        self.mic_label.move(
            (self.width() - self.mic_label.width()) // 2,
            self.height() - 200
        )

    # ==================================================
    # TEXT
    # ==================================================

    def add_text(self, text: str):
        if text:
            self.text_buffer += text
            self.refresh_text_display()

    def refresh_text_display(self):
        self.text_area.setPlainText(self.text_buffer)
        cursor = self.text_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_area.setTextCursor(cursor)

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
        if not self.typing_active:
            return
        if action == Action.INSERT_CHAR:
            self.add_text(value)

        elif action == Action.SPACE:
            self.add_text(" ")

        elif action == Action.BACKSPACE:
            self.text_buffer = self.text_buffer[:-1]
            self.text_area.setPlainText(self.text_buffer)
            cursor = self.text_area.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.text_area.setTextCursor(cursor)

        elif action == Action.DONE:
            self.keyboard.hide()
            self.typing_active = False
            self.suggestion_bar.update_suggestions([])
            return
        # After updating text, compute suggestions
        suggestions = self.predictor.get_suggestions(self.text_buffer)
        self.suggestion_bar.update_suggestions(suggestions)

    def on_suggestion_selected(self, word):
        if not self.typing_active:
            return

        context, prefix = extract_context_and_prefix(self.text_buffer)

        if prefix:
            self.text_buffer = self.text_buffer[:-len(prefix)]

        self.text_buffer += word + " "

        self.refresh_text_display()

        suggestions = self.predictor.get_suggestions(self.text_buffer)
        self.suggestion_bar.update_suggestions(suggestions)

class NotesFocusArea(FocusableWidget):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.setGeometry(widget.geometry())

    def select(self):
        return Action.SELECT
