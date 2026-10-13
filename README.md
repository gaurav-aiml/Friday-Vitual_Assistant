# Friday - Virtual Assistant

Friday is a voice-controlled personal assistant for Linux desktops. It can respond
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
│   └── test_linux_compat.py
└── todos.json             # created at runtime when you use todo commands
```

## Requirements

- Linux desktop with an active graphical user session
- Python 3.10+
- Microphone access
- Internet connection for Google Speech Recognition
- An active user session for microphone, clipboard, display, and power controls

## Linux setup

On Debian or Ubuntu, install the system packages needed for microphone, speech,
audio, and clipboard support:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-dev portaudio19-dev espeak-ng \
  libasound2-dev xclip
```

Create a virtual environment and install the Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run Friday from a logged-in desktop session:

```bash
python friday.py
```

`pyttsx3` uses the installed eSpeak speech engine. Volume control uses `wpctl`
(PipeWire) or `pactl` (PulseAudio/PipeWire PulseAudio); brightness control uses
`brightnessctl` and may require additional device permissions. The lock, sleep,
and shutdown actions use `loginctl`, `systemctl`, and `shutdown` and depend on
the desktop session and system policy.

Clipboard operations use the Linux desktop clipboard via `pyperclip`; install
`xclip`, `xsel`, or `wl-clipboard` as appropriate for your X11 or Wayland
session. Screen capture uses `pyautogui` and works best with a visible X11
desktop; screen capture support can vary under Wayland. Microphone input and
Google Speech Recognition require a working microphone and internet connection,
respectively.

## Run tests

With the virtual environment active, run:

```bash
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

- Some features require the Linux system utilities, desktop session, or device
  permissions described above.
- Destructive actions such as shutdown should be used with care.
- Use `Ctrl+C` in the terminal to stop the assistant.
