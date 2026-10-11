import datetime
import os
import platform
import re
import subprocess
import webbrowser

import pyttsx3
import speech_recognition as sr

from storage import todos

# ---------------------------------------------------------------------------
# Core assistant setup
# ---------------------------------------------------------------------------

def create_engine() -> pyttsx3.Engine:
    driver = "sapi5" if platform.system() == "Windows" else None
    engine = pyttsx3.init(driver)
    engine.setProperty("rate", 125)
    return engine


engine = create_engine()


def speak(audio: str) -> None:
    engine.say(audio)
    engine.runAndWait()


def greet() -> None:
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 17:
        speak("Good afternoon")
    elif 17 <= hour < 21:
        speak("Good evening")
    else:
        speak("Good Night")


recognizer = sr.Recognizer()


def listen() -> sr.AudioData | None:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return audio
    except sr.WaitTimeoutError:
        print("No speech detected; listening again.")
        return None


# ---------------------------------------------------------------------------
# Wikipedia feature
# ---------------------------------------------------------------------------

def handle_wikipedia(query: str) -> str | None:
    trigger = None
    for phrase in ("who is ", "what is ", "wikipedia ", "tell me about "):
        if phrase in query:
            trigger = phrase
            break
    if not trigger:
        return None

    try:
        import wikipedia
    except ImportError:
        return "Wikipedia lookup requires the wikipedia package."

    topic = query.split(trigger, 1)[1].strip()
    topic = " ".join(part for part in topic.split() if part.lower() not in {"the", "a", "an"})
    if not topic:
        return "I couldn't find a topic to look up."

    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as exc:
        options = ", ".join(exc.options[:3])
        return f"Multiple matches: {options}"
    except wikipedia.exceptions.PageError:
        return f"Sorry, no Wikipedia page for {topic}."
    except Exception as exc:  # pragma: no cover
        return f"Wikipedia error: {exc}"


# ---------------------------------------------------------------------------
# Volume and brightness feature
# ---------------------------------------------------------------------------

def _get_windows_volume() -> int:
    try:
        from ctypes import POINTER, cast
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return int(volume.GetMasterVolumeLevelScalar() * 100)
    except ImportError:
        return 0


def _set_windows_volume(level: int) -> None:
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100, None)


def _get_brightness() -> int:
    try:
        import screen_brightness_control as sbc

        return int(sbc.get_brightness()[0])
    except ImportError:
        return 0


def _set_brightness(level: int) -> None:
    try:
        import screen_brightness_control as sbc

        sbc.set_brightness(level)
    except ImportError:
        return None


def handle_system_control(query: str) -> str | None:
    text = query.lower()

    if "volume" in text:
        current = _get_windows_volume() if platform.system() == "Windows" else 0
        if "up" in text:
            new_level = min(100, current + 10)
            if platform.system() == "Windows":
                _set_windows_volume(new_level)
            else:
                os.system(f"osascript -e 'set volume output volume {new_level}'")
            return f"Volume at {new_level}%"
        if "down" in text:
            new_level = max(0, current - 10)
            if platform.system() == "Windows":
                _set_windows_volume(new_level)
            else:
                os.system(f"osascript -e 'set volume output volume {new_level}'")
            return f"Volume at {new_level}%"
        if "mute" in text:
            if platform.system() == "Windows":
                _set_windows_volume(0)
            else:
                os.system("osascript -e 'set volume output volume 0'")
            return "Muted"

        for token in text.split():
            if token.isdigit():
                level = int(token)
                if platform.system() == "Windows":
                    _set_windows_volume(level)
                else:
                    os.system(f"osascript -e 'set volume output volume {level}'")
                return f"Volume set to {level}%"

    if "brightness" in text:
        current = _get_brightness()
        if "up" in text:
            new_level = min(100, current + 10)
            _set_brightness(new_level)
            return f"Brightness at {new_level}%"
        if "down" in text:
            new_level = max(0, current - 10)
            _set_brightness(new_level)
            return f"Brightness at {new_level}%"

        for token in text.split():
            if token.isdigit():
                level = int(token)
                _set_brightness(level)
                return f"Brightness at {level}%"

    return None


# ---------------------------------------------------------------------------
# Screenshot feature
# ---------------------------------------------------------------------------

def handle_screenshot(query: str) -> str | None:
    if "screenshot" not in query and "capture screen" not in query:
        return None

    try:
        import pyautogui
    except ImportError:
        return "Screenshot requires pyautogui and pillow."

    save_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Friday")
    os.makedirs(save_dir, exist_ok=True)
    filename = f"screenshot_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
    path = os.path.join(save_dir, filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved to {filename}"


# ---------------------------------------------------------------------------
# Power control feature
# ---------------------------------------------------------------------------

def handle_power_control(query: str) -> str | None:
    text = query.lower()
    system = platform.system()

    if "shutdown abort" in text or "cancel shutdown" in text:
        if system == "Windows":
            os.system("shutdown /a")
        return "Shutdown cancelled."

    if "lock" in text and ("pc" in text or "screen" in text):
        if system == "Windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif system == "Darwin":
            os.system("pmset displaysleepnow")
        else:
            os.system("loginctl lock-session")
        return "Locking your PC."

    if "shutdown" in text or "shut down" in text:
        if system == "Windows":
            os.system("shutdown /s /t 5")
        else:
            os.system("shutdown -h +1")
        return "Shutting down in 5 seconds. Say 'shutdown abort' to cancel."

    if "sleep" in text and ("pc" in text or "mode" in text):
        if system == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif system == "Darwin":
            os.system("pmset sleepnow")
        else:
            os.system("systemctl suspend")
        return "Going to sleep."

    return None


# ---------------------------------------------------------------------------
# App launcher feature
# ---------------------------------------------------------------------------

def handle_app_launcher(query: str) -> str | None:
    if not any(word in query for word in ("open ", "launch ", "start ")):
        return None

    app_map = {
        "chrome": {"Windows": "chrome", "Darwin": "Google Chrome", "Linux": "google-chrome"},
        "vscode": {"Windows": "code", "Darwin": "Visual Studio Code", "Linux": "code"},
        "notepad": {"Windows": "notepad", "Darwin": "TextEdit", "Linux": "gedit"},
        "spotify": {"Windows": "spotify", "Darwin": "Spotify", "Linux": "spotify"},
        "calculator": {"Windows": "calc", "Darwin": "Calculator", "Linux": "gnome-calculator"},
        "terminal": {"Windows": "cmd", "Darwin": "Terminal", "Linux": "gnome-terminal"},
        "explorer": {"Windows": "explorer", "Darwin": "Finder", "Linux": "nautilus"},
    }

    text = query.lower()
    for app_name, platform_map in app_map.items():
        if app_name in text:
            os_name = platform.system()
            target = platform_map.get(os_name)
            if not target:
                return f"{app_name} is not mapped for {os_name}."
            try:
                if os_name == "Windows":
                    os.startfile(target)
                elif os_name == "Darwin":
                    subprocess.Popen(["open", "-a", target])
                else:
                    subprocess.Popen([target])
                return f"Opening {app_name}."
            except Exception as exc:
                return f"Couldn't open {app_name}: {exc}"
    return None


# ---------------------------------------------------------------------------
# Battery feature
# ---------------------------------------------------------------------------

def handle_battery(query: str) -> str | None:
    if "battery" not in query:
        return None

    try:
        import psutil
    except ImportError:
        return "Battery status requires psutil."

    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected — desktop PC."

    status = "plugged in" if battery.power_plugged else "on battery"
    return f"Battery at {int(battery.percent)} percent, {status}."


# ---------------------------------------------------------------------------
# Clipboard feature
# ---------------------------------------------------------------------------

def handle_clipboard(query: str) -> str | None:
    text = query.lower()
    if "clipboard" not in text:
        return None

    try:
        import pyperclip
    except ImportError:
        return "Clipboard features require pyperclip."

    if any(word in text for word in ("what", "read", "show")):
        content = pyperclip.paste()
        if not content.strip():
            return "Clipboard is empty."
        preview = content[:200] + ("..." if len(content) > 200 else "")
        return f"Clipboard contains: {preview}"

    if "clear" in text or "empty" in text:
        pyperclip.copy("")
        return "Clipboard cleared."

    if "copy" in text:
        for separator in ("clipboard ", "clipboard:"):
            if separator in text:
                content = query.split(separator, 1)[1].strip()
                pyperclip.copy(content)
                return f"Copied: {content[:50]}"

    return None


# ---------------------------------------------------------------------------
# WhatsApp feature
# ---------------------------------------------------------------------------

def handle_whatsapp(query: str) -> str | None:
    if "whatsapp" not in query:
        return None

    contacts = {"mom": "+919999999999", "dad": "+918888888888", "rahul": "+917777777777"}
    match = re.search(r"to\s+(\w+).*?(?:saying|that|message)\s+(.+)", query, flags=re.IGNORECASE)
    if not match:
        return "Say: send whatsapp to <name> saying <message>"

    name, message = match.group(1).lower(), match.group(2).strip()
    phone = contacts.get(name)
    if not phone:
        return f"No number saved for {name}."

    try:
        import pywhatkit

        pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=True)
        return f"Message sent to {name}."
    except Exception as exc:  # pragma: no cover
        return f"WhatsApp failed: {exc}"


# ---------------------------------------------------------------------------
# Main command dispatcher
# ---------------------------------------------------------------------------

def handle_command(query: str) -> str | None:
    query = query.lower().strip()
    if not query:
        return None

    if query.startswith("add task "):
        task = query.replace("add task ", "", 1).strip()
        return todos.add_task(task)

    if query.startswith(("complete task ", "done task ", "finish task ")):
        try:
            task_id = int(query.split()[-1])
            return todos.complete_task(task_id)
        except ValueError:
            return "Please say the task number."

    if "clear" in query and "task" in query:
        return todos.clear_done()

    if ("task" in query or "todo" in query) and any(
        word in query for word in ("show", "list", "my", "what")
    ):
        return todos.list_tasks()

    for handler in (
        handle_whatsapp,
        handle_clipboard,
        handle_power_control,
        handle_screenshot,
        handle_system_control,
        handle_battery,
        handle_wikipedia,
        handle_app_launcher,
    ):
        response = handler(query)
        if response:
            return response

    if "open browser" in query:
        webbrowser.open("https://www.google.com")
        return "Opening browser."
    if "open linkedin" in query:
        webbrowser.open("https://www.linkedin.com/in/gauravaiml")
        return "Opening LinkedIn."
    if "open github" in query:
        webbrowser.open("https://www.github.com/gaurav-aiml")
        return "Opening GitHub."
    if "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    if "open my channel" in query:
        webbrowser.open("https://www.youtube.com/@gaurav-aiml")
        return "Opening your channel."

    return "I didn't catch that, Sir."


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    greet()
    speak("Hello Sir, I am Friday...")
    while True:
        audio = listen()
        if audio is None:
            continue

        try:
            query = recognizer.recognize_google(audio_data=audio, language="en-US").lower()
        except sr.UnknownValueError:
            print("Background Noise! Can't Listen")
            continue
        except sr.RequestError as exc:
            print(f"Speech recognition service unavailable: {exc}")
            continue

        response = handle_command(query)
        if response:
            print(response)
            speak(response)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFriday stopped.")
