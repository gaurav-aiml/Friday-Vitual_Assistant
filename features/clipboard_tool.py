"""Clipboard helper commands."""

from __future__ import annotations


def handle_command(query: str) -> str | None:
    text = query.lower()
    if "clipboard" not in text:
        return None

    try:
        import pyperclip
    except ImportError:
        return "Clipboard features require pyperclip."

    try:
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
    except pyperclip.PyperclipException as exc:
        return (
            f"Clipboard unavailable: {exc}. On Windows 11, ensure the app has"
            " clipboard access and try again."
        )

    return None
