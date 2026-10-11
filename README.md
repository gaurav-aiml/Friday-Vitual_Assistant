# Friday - Virtual Assistant

Friday is a voice-activated assistant that can open websites in your default
browser. It supports Windows 11 and Linux.

## Windows 11 setup

Install Python 3.10 or later, then open PowerShell in the project directory and
create and activate a virtual environment:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, allow scripts for the current PowerShell
session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Start Friday from the project directory:

```powershell
python friday.py
```

Allow microphone access for desktop apps in **Settings > Privacy & security >
Microphone**. Friday uses Windows' SAPI5 speech engine for audio output.

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

Friday uses the default microphone for voice input. On Linux, `pyttsx3` uses
the installed speech driver (for example, `espeak`). On both platforms,
`SpeechRecognition` sends recognized speech to Google's speech-recognition
service, so an internet connection is required. Use `Ctrl+C` to stop the
assistant.
