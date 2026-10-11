# Friday - Virtual Assistant

Friday is a voice-controlled personal assistant for Windows and Linux. It can
respond to spoken commands for todo actions, web browsing, Wikipedia lookups,
system controls, app launching, screen capture, clipboard access, and more.

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
└── todos.json             # created at runtime when you use todo commands
```

## Requirements

- Python 3.10+
- Microphone access
- Internet connection for Google Speech Recognition
- Optional system tools for some features:
  - `espeak-ng` on Linux
  - system-level commands for lock/shutdown/sleep

## Windows setup

Open PowerShell in the project directory and run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If script execution is blocked, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Then start the assistant:

```powershell
python friday.py
```

Allow microphone access in Settings > Privacy & security > Microphone so the
assistant can listen for commands. Friday uses Windows SAPI5 for speech output.

## Linux setup

Install Python and a speech backend if needed:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip espeak-ng
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the assistant:

```bash
python friday.py
```

On Linux, `pyttsx3` relies on the available speech engine (for example,
`espeak`). A working internet connection is required for Google speech
recognition.

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

- Some features may require the relevant Python packages to be installed and,
  for some operating systems, the associated system utilities to be available.
- Destructive actions such as shutdown should be used with care.
- Use `Ctrl+C` in the terminal to stop the assistant.
