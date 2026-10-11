"""Screen capture feature."""

from __future__ import annotations

import os
from datetime import datetime

SAVE_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "Friday")


def handle_command(query: str) -> str | None:
    if "screenshot" not in query and "capture screen" not in query:
        return None

    try:
        import pyautogui
    except ImportError:
        return "Screenshot requires pyautogui and pillow."

    os.makedirs(SAVE_DIR, exist_ok=True)
    filename = f"screenshot_{datetime.now():%Y%m%d_%H%M%S}.png"
    path = os.path.join(SAVE_DIR, filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved to {filename}"
