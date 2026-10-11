"""Power control commands: lock, sleep, shutdown."""

from __future__ import annotations

import os
import platform


def handle_command(query: str) -> str | None:
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
