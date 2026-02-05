import pyttsx3
import threading

_lock = threading.Lock()


def speak(text: str):
    def _run():
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    with _lock:
        t = threading.Thread(target=_run, daemon=True)
        t.start()


def reset_tts():
    pass  # no-op, engine is recreated each time
