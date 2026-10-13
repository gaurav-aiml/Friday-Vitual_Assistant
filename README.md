# Friday - Virtual Assistant

Friday is a voice-controlled personal assistant for Windows 11. It can respond
to spoken commands for todo actions, web browsing, Wikipedia lookups, system
controls, app launching, screen capture, clipboard access, and more.

## Features

- Voice input with microphone listening
- Text-to-speech output with `pyttsx3`
- Todo list management
- Open websites and popular profiles
- Wikipedia summary queries
- Volume and brightness controls
- Screenshot capture
- Lock, shutdown, and sleep actions
- Launch installed applications
- Battery status reporting
- Clipboard read/copy/clear support
- WhatsApp message sending via browser automation

## Project structure

```text
Friday-Vitual_Assistant/
├── friday.py               # Main entry point and command dispatcher
├── app/
│   └── friday.py           # Compatibility wrapper
├── core/
│   └── tools.py            # Shared command routing
├── features/
│   ├── app_launcher.py
│   ├── battery.py
│   ├── clipboard_tool.py
│   ├── power_control.py
│   ├── screenshot.py
│   ├── system_control.py
│   ├── whatsapp.py
│   ├── wikipedia_tool.py
│   └── __init__.py
├── storage/
│   ├── todos.py
│   └── __init__.py
├── requirements.txt
├── README.md
├── tests/
│   └── test_windows_compat.py
└── todos.json             # created at runtime when you use todo commands
```

## Requirements

- Windows 11 desktop
- Python 3.10+
- Microphone access
- Internet connection for Google Speech Recognition
- An active user session for microphone, clipboard, display, and power controls

## Windows 11 setup

Open PowerShell in the project directory.

Create a virtual environment and install the project dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run Friday from a logged-in desktop session:

```powershell
python friday.py
```

`pyttsx3` uses the installed Windows speech engine. The volume and brightness
controls rely on PowerShell and the Windows audio/display APIs available on
Windows 11. The shutdown and sleep actions use native Windows commands such as
`shutdown` and `rundll32.exe`, and may require administrator privileges or a
logged-in session.

Clipboard operations use the Windows system clipboard via `pyperclip`. Screen
capture uses `pyautogui` and works best when the desktop is visible and
permissions are enabled. Microphone input and Google Speech Recognition require
a working microphone and internet connection, respectively.

## Run tests

With the virtual environment active in PowerShell, run:

```powershell
python -m unittest discover -s tests -v
```

## Example commands

- "add task buy milk"
- "show my tasks"
- "complete task 2"
- "open browser"
- "open github"
- "who is Albert Einstein"
- "volume up"
- "set brightness 50"
- "take screenshot"
- "lock pc"
- "shutdown pc"
- "battery status"
- "read clipboard"
- "send whatsapp to mom saying hello"

## Notes

- Some features require the relevant Windows 11 system utilities, desktop session,
  or device permissions described above.
- Destructive actions such as shutdown should be used with care.
- Use `Ctrl+C` in the terminal to stop the assistant.
