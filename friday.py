"""Voice-controlled entry point for the Friday assistant."""

from __future__ import annotations

import datetime

import pyttsx3
import speech_recognition as sr

from core.tools import handle_command


def create_engine() -> pyttsx3.Engine:
    engine = pyttsx3.init()
    engine.setProperty("rate", 125)
    return engine


engine = create_engine()
recognizer = sr.Recognizer()


def speak(audio: str) -> None:
    engine.say(audio)
    engine.runAndWait()


def greet() -> None:
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 17:
        speak("Good afternoon")
    elif 17 <= hour < 21:
        speak("Good evening")
    else:
        speak("Good Night")


def listen() -> sr.AudioData | None:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return recognizer.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        print("No speech detected; listening again.")
        return None


def main() -> None:
    greet()
    speak("Hello Sir, I am Friday...")
    while True:
        try:
            audio = listen()
        except OSError as exc:
            print(f"Microphone unavailable: {exc}")
            return

        if audio is None:
            continue

        try:
            query = recognizer.recognize_google(audio_data=audio, language="en-US").lower()
        except sr.UnknownValueError:
            print("Background Noise! Can't Listen")
            continue
        except sr.RequestError as exc:
            print(f"Speech recognition service unavailable: {exc}")
            continue

        response = handle_command(query)
        if response:
            print(response)
            speak(response)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFriday stopped.")
