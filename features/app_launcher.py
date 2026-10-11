"""Open installed applications."""

from __future__ import annotations

import shutil
import subprocess

APP_MAP = {
    "chrome": ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"),
    "vscode": ("code",),
    "notepad": ("gnome-text-editor", "gedit", "mousepad"),
    "spotify": ("spotify",),
    "calculator": ("gnome-calculator",),
    "terminal": ("kgx", "gnome-terminal", "x-terminal-emulator"),
    "explorer": ("nautilus",),
}


def _find_linux_command(candidates: tuple[str, ...]) -> str | None:
    return next((path for name in candidates if (path := shutil.which(name))), None)


def handle_command(query: str) -> str | None:
    if not any(word in query for word in ("open ", "launch ", "start ")):
        return None

    text = query.lower()
    for app_name, candidates in APP_MAP.items():
        if app_name not in text:
            continue

        try:
            target = _find_linux_command(candidates)
            if target is None:
                return (
                    f"Couldn't open {app_name}: no supported application "
                    f"was found ({', '.join(candidates)})."
                )
            subprocess.Popen([target])
            return f"Opening {app_name}."
        except OSError as exc:
            return f"Couldn't open {app_name}: {exc}"

    return None
