from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from app.ui.widgets.mic_button import MicButton
from app.ui.widgets.back_button import BackButton
from core.audio.stt import VoiceWorker


class VoiceNotesScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ================= Background =================
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#8D8686"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # ================= Title =================
        self.title = QLabel("VOICE NOTES", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setGeometry(0, 20, 1400, 60)
        self.title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: black;
        """)

        # ================= Text Area =================
        self.text_area = QTextEdit(self)
        self.text_area.setGeometry(200, 520, 1000, 120)
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            background-color: #2E2E2E;
            color: white;
            font-size: 18px;
            border-radius: 20px;
            padding: 15px;
        """)

        # ================= Mic Button =================
        self.mic_button = MicButton(self)
       # self.mic_button.clicked.connect(self.toggle_voice_input)  # IMPORTANT

        # ================= Recording Label =================
        self.mic_label = QLabel("🎤 Recording...", self)
        self.mic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mic_label.setStyleSheet("""
            font-size: 28px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 20px;
            border-radius: 20px;
        """)
        self.mic_label.hide()

        # ================= Back Button =================
        self.back_button = BackButton(self)
        self.back_button.move(20, 20)

        # ================= Focusables =================
        self.focusables = [self.mic_button, self.back_button]

        # ================= Voice State =================
        self.voice_active = False
        self.voice_worker = None

    # ==================================================
    # VOICE CONTROL
    # ==================================================
    def toggle_voice_input(self):
        if self.voice_active:
            self.stop_voice_input()
        else:
            self.start_voice_input()

    def start_voice_input(self):
        if self.voice_active:
            return

        print("Voice started")  # Debug

        self.voice_active = True
        self.mic_button.set_recording(True)

        self.center_mic_label()
        self.mic_label.show()

        # Start worker thread
        self.voice_worker = VoiceWorker()
        self.voice_worker.finished.connect(self.on_voice_result)
        self.voice_worker.start()

    def stop_voice_input(self):
        if self.voice_worker:
            self.voice_worker.stop()

    def on_voice_result(self, text):
        print("Voice finished:", text)  # Debug

        self.voice_active = False
        self.mic_button.set_recording(False)
        self.mic_label.hide()

        if text and text.strip():
            self.text_area.insertPlainText(text + " ")

        self.voice_worker = None

    # ==================================================
    # CENTERING LOGIC
    # ==================================================
    def center_mic(self):
        x = (self.width() - self.mic_button.width()) // 2
        y = (self.height() - self.mic_button.height()) // 2 - 40
        self.mic_button.move(x, y)

    def center_mic_label(self):
        self.mic_label.adjustSize()
        x = (self.width() - self.mic_label.width()) // 2
        y = self.mic_button.y() - 80
        self.mic_label.move(x, y)

    # ==================================================
    # EVENTS
    # ==================================================
    def showEvent(self, event):
        super().showEvent(event)
        self.center_mic()
        self.center_mic_label()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.center_mic()
        self.center_mic_label()