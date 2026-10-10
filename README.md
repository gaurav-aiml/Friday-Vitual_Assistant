# Friday - Virtual Assistant

Friday is a voice-activated assistant that can open websites in your default
browser.

## Linux setup

Install Python 3.10 or later and a system text-to-speech backend such as
`espeak-ng` so `pyttsx3` can initialize correctly on Linux.

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip espeak-ng
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start Friday from the project directory:

```bash
python friday.py
```

Friday uses the default microphone for voice input and the system's default
speech engine for audio output. On Linux, `pyttsx3` will use the available
installed driver (for example `espeak`). `SpeechRecognition` sends recognized
speech to Google's speech-recognition service, so an internet connection is
required. Use `Ctrl+C` to stop the assistant.
