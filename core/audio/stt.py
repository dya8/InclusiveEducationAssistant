import speech_recognition as sr


def listen_once(timeout=5) -> str | None:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None

    try:
        text = r.recognize_google(audio)
        print("Recognized:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("STT error:", e)
        return None
