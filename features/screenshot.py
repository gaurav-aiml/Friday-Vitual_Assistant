"""Screen capture feature."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

SAVE_DIR = Path.home() / "Pictures" / "Friday"


def handle_command(query: str) -> str | None:
    if "screenshot" not in query and "capture screen" not in query:
        return None

    try:
        import pyautogui
    except ImportError:
        return "Screenshot requires pyautogui and pillow."

    try:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"screenshot_{datetime.now():%Y%m%d_%H%M%S}.png"
        path = SAVE_DIR / filename
        pyautogui.screenshot(str(path))
    except (OSError, RuntimeError) as exc:
        return (
            f"Couldn't capture the screen: {exc}. On Windows 11, make sure the "
            "desktop is visible and screen capture permissions are enabled."
        )
    return f"Screenshot saved to {filename}"
