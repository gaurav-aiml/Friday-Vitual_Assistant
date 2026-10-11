"""Open installed applications."""

from __future__ import annotations

import os
import platform
import subprocess

APP_MAP = {
    "chrome": {"Windows": "chrome", "Darwin": "Google Chrome", "Linux": "google-chrome"},
    "vscode": {"Windows": "code", "Darwin": "Visual Studio Code", "Linux": "code"},
    "notepad": {"Windows": "notepad", "Darwin": "TextEdit", "Linux": "gedit"},
    "spotify": {"Windows": "spotify", "Darwin": "Spotify", "Linux": "spotify"},
    "calculator": {"Windows": "calc", "Darwin": "Calculator", "Linux": "gnome-calculator"},
    "terminal": {"Windows": "cmd", "Darwin": "Terminal", "Linux": "gnome-terminal"},
    "explorer": {"Windows": "explorer", "Darwin": "Finder", "Linux": "nautilus"},
}


def handle_command(query: str) -> str | None:
    if not any(word in query for word in ("open ", "launch ", "start ")):
        return None

    text = query.lower()
    for app_name, platform_map in APP_MAP.items():
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
