import pyttsx3
import speech_recognition as sr

from tools import handle_command

engine = pyttsx3.init()
engine.setProperty("rate", 125)
voices = engine.getProperty("voice")
engine.setProperty("voice", voices[1])


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

r = sr.Recognizer()
def listen():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            speak("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            return audio
    except sr.UnknownValueError:
        print("Didn't Listen")


def main():
    while True:
        audio = listen()
        try:
            query = r.recognize_google(audio_data=audio, language="en-US").lower()
        except sr.UnknownValueError:
            print("Background Noise! Can't Listen")
            continue
        
        handle_command(query)


if __name__ == "__main__":
    main()