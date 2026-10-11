# Friday - Virtual Assistant

Friday is a voice-controlled personal assistant for Ubuntu 26.04. It can respond
to spoken commands for todo actions, web browsing, Wikipedia lookups, system
controls, app launching, screen capture, clipboard access, and more. Friday is
Linux-only; Windows and macOS are not supported.

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

- Ubuntu 26.04 desktop (GNOME recommended)
- Python 3.10+
- Microphone access
- Internet connection for Google Speech Recognition
- A logged-in graphical session for microphone, clipboard, display, and power
  controls

## Ubuntu 26.04 setup

Open a terminal in the project directory.

Install the Python build tools and system utilities used by voice input, speech
output, audio/display controls, screenshots, and clipboard access:

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  brightnessctl \
  espeak-ng \
  libespeak1 \
  portaudio19-dev \
  pulseaudio-utils \
  python3-dev \
  python3-pip \
  python3-tk \
  python3-venv \
  python3-xlib \
  scrot \
  wl-clipboard \
  xclip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run Friday from a logged-in graphical desktop session:

```bash
python3 friday.py
```

`pyttsx3` uses `espeak-ng` for speech output. `PyAudio` is built against
PortAudio in the virtual environment. Ubuntu's PipeWire audio service provides
the PulseAudio-compatible interface used by `pactl`; install and run an audio
session for volume controls. `brightnessctl` needs a supported backlight
device and appropriate permissions. The power actions use Ubuntu's
`loginctl`, `shutdown`, and `systemctl` commands and may be restricted by
session or administrator policy.

Clipboard commands use `wl-clipboard` in Wayland sessions or `xclip` in X11
sessions. PyAutoGUI screen capture depends on an X11 display and may be blocked
or limited in a Wayland session; if capture fails, it may require an X11
session. Microphone input and Google Speech Recognition require a working
microphone and internet connection, respectively.

## Run tests

With the project virtual environment active, run:

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

- Some features require the relevant Ubuntu system utilities, desktop session,
  or device permissions described above.
- Destructive actions such as shutdown should be used with care.
- Use `Ctrl+C` in the terminal to stop the assistant.
