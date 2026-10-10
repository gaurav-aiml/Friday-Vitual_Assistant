import datetime
import pyttsx3

engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 125)


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