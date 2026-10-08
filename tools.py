import webbrowser

import pyttsx3
import speech_recognition as sr

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
            print("Listening...")
            audio = r.listen(source, timeout=5,phrase_time_limit=10)
            return audio
    except sr.UnknownValueError:  
        print("Didn't Listen")

def handle_command(query):
    while True:
        try:
            audio=listen()
            query = r.recognize_google(audio_data=audio, language="en-US").lower()

        except sr.UnknownValueError:
            print("Background Noise! Can't Listen")

        if 'open browser' in query:
            webbrowser.open("www.google.com")

        elif 'open linkedin' in query:
            webbrowser.open('www.linkedin.com/in/gauravaiml')

        elif 'open github' in query:
            webbrowser.open('www.github.com/gaurav-aiml')

        elif 'open youtube' in query:
            webbrowser.open('www.youtube.com')

        elif 'open my channel' in query:
            webbrowser.open('https://www.youtube.com/@gaurav-aiml')