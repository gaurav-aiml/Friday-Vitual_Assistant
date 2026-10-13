from __future__ import annotations

import shutil
import subprocess

APP_MAP = {
    "chrome": ("chrome.exe", "msedge.exe", "brave.exe", "firefox.exe"),
    "vscode": ("code.exe", "code.cmd", "Code.exe"),
    "notepad": ("notepad.exe",),
    "spotify": ("spotify.exe",),
    "calculator": ("calc.exe",),
    "terminal": ("wt.exe", "cmd.exe", "powershell.exe"),
    "explorer": ("explorer.exe",),
}


def _find_windows_command(candidates: tuple[str, ...]) -> str | None:
    return next((path for name in candidates if (path := shutil.which(name))), None)


def handle_command(query: str) -> str | None:
    if not any(word in query for word in ("open ", "launch ", "start ")):
        return None

    text = query.lower()
    for app_name, candidates in APP_MAP.items():
        if app_name not in text:
            continue

        try:
            target = _find_windows_command(candidates)
            if target is None:
                return (
                    f"Couldn't open {app_name}: no supported app was found "
                    f"({', '.join(candidates)})."
                )
            subprocess.Popen([target])
            return f"Opening {app_name}."
        except OSError as exc:
            return f"Couldn't open {app_name}: {exc}"

    return None
