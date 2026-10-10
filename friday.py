import platform

import pyttsx3
import speech_recognition as sr
from greet_friday import greet

from tools import handle_command


def create_engine() -> pyttsx3.Engine:
    driver = "sapi5" if platform.system() == "Windows" else None
    engine = pyttsx3.init(driver)
    engine.setProperty("rate", 125)
    return engine


engine = create_engine()


def speak(audio: str) -> None:
    engine.say(audio)
    engine.runAndWait()


recognizer = sr.Recognizer()

greet()
def listen() -> sr.AudioData | None:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            speak("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return audio
    except sr.WaitTimeoutError:
        print("No speech detected; listening again.")
        return None


def main() -> None:
    while True:
        audio = listen()
        if audio is None:
            continue

        try:
            query = recognizer.recognize_google(
                audio_data=audio, language="en-US"
            ).lower()
        except sr.UnknownValueError:
            print("Background Noise! Can't Listen")
            continue
        except sr.RequestError as exc:
            print(f"Speech recognition service unavailable: {exc}")
            continue

        handle_command(query)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFriday stopped.")
