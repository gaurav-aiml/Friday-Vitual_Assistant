from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path

AppConfig = tuple[tuple[str, ...], tuple[str, ...]]

LINUX_APP_MAP: dict[str, AppConfig] = {
    "chrome": (
        (
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "microsoft-edge",
            "brave-browser",
            "firefox",
        ),
        (),
    ),
    "vscode": (("code",), ()),
    "notepad": (("gnome-text-editor", "gedit", "mousepad", "kate"), ()),
    "spotify": (("spotify",), ()),
    "calculator": (("gnome-calculator", "kcalc", "galculator"), ()),
    "terminal": (
        ("x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal"),
        (),
    ),
    "explorer": (("xdg-open",), (str(Path.home()),)),
}

WINDOWS_APP_MAP: dict[str, AppConfig] = {
    "chrome": (("chrome.exe", "msedge.exe", "brave.exe", "firefox.exe"), ()),
    "vscode": (("code.exe", "code.cmd"), ()),
    "notepad": (("notepad.exe",), ()),
    "spotify": (("Spotify.exe", "spotify.exe"), ()),
    "calculator": (("calc.exe",), ()),
    "terminal": (("wt.exe", "powershell.exe", "cmd.exe"), ()),
    "explorer": (("explorer.exe",), (str(Path.home()),)),
}


def _find_command(candidates: tuple[str, ...]) -> str | None:
    return next((path for name in candidates if (path := shutil.which(name))), None)


def handle_command(query: str) -> str | None:
    if not any(word in query for word in ("open ", "launch ", "start ")):
        return None

    text = query.lower()
    app_map: dict[str, AppConfig] = (
        WINDOWS_APP_MAP if platform.system() == "Windows" else LINUX_APP_MAP
    )
    for app_name, (candidates, arguments) in app_map.items():
        if app_name not in text:
            continue

        try:
            target = _find_command(candidates)
            if target is None:
                return (
                    f"Couldn't open {app_name}: no supported app was found "
                    f"({', '.join(candidates)})."
                )
            command = [target, *arguments]
            if (
                platform.system() == "Windows"
                and target.lower().endswith((".cmd", ".bat"))
            ):
                command = [os.environ.get("COMSPEC", "cmd.exe"), "/c", *command]
            subprocess.Popen(command)
            return f"Opening {app_name}."
        except OSError as exc:
            return f"Couldn't open {app_name}: {exc}"

    return None
