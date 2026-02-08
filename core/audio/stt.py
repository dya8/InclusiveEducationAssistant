import speech_recognition as sr
from PyQt6.QtCore import QThread, pyqtSignal


class VoiceWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._stop_requested = False

    def run(self):
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)

                audio = r.listen(source)

                if self._stop_requested:
                    self.finished.emit("")
                    return

                try:
                    text = r.recognize_google(audio)
                    self.finished.emit(text)
                except sr.UnknownValueError:
                    self.finished.emit("")
                except sr.RequestError:
                    self.finished.emit("")

        except Exception:
            self.finished.emit("")

    def stop(self):
        self._stop_requested = True
