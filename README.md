# Friday - Virtual Assistant

Friday is a voice-activated assistant that can open websites in your default
browser.

## Windows setup

Install Python 3.10 or later and make sure the Python launcher (`py`) is
available. From PowerShell in the project directory, create and activate a
virtual environment, then install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation scripts, run this once for the current user,
then activate the environment again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Start Friday from the project directory:

```powershell
python .\friday.py
```

Friday uses the default microphone and Windows SAPI5 speech output.
`SpeechRecognition` sends recognized speech to Google's speech-recognition
service, so an internet connection is required. Use `Ctrl+C` to stop the
assistant.
