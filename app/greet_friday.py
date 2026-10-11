import datetime
import platform

import pyttsx3


def create_engine() -> pyttsx3.Engine:
    driver = "sapi5" if platform.system() == "Windows" else None
    engine = pyttsx3.init(driver)
    engine.setProperty("rate", 125)
    return engine


engine = create_engine()


def speak(audio: str) -> None:
    engine.say(audio)
    engine.runAndWait()


def greet():
    hour = datetime.datetime.now().hour
    
    if 5 <= hour < 12:
        speak('Good Morning')
    elif 12 <= hour < 17:
        speak("Good afternoon")
    elif 17 <= hour < 21:
        speak("Good evening")
    else:
        speak("Good Night")