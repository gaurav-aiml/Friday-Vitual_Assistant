# Friday - Virtual Assistant

Friday is a voice-activated assistant that can open websites in your default
browser.

## Ubuntu 26.04 setup

Install the system libraries used by microphone capture and speech output:

```bash
sudo apt update
sudo apt install python3-venv python3-dev portaudio19-dev espeak-ng libespeak1
```

Create a virtual environment and install the Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start Friday from the project directory:

```bash
python friday.py
```

Friday uses the default microphone and speaker. `SpeechRecognition` sends
recognized speech to Google's speech-recognition service, so an internet
connection is required. Use `Ctrl+C` to stop the assistant.
