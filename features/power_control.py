"""Power control commands: lock, sleep, shutdown."""

from __future__ import annotations

import subprocess


def _run_command(command: list[str]) -> None:
    subprocess.run(command, check=True, capture_output=True, text=True)


def _error_message(action: str, exc: Exception) -> str:
    detail = getattr(exc, "stderr", None)
    if detail:
        detail = detail.strip()
    if isinstance(exc, FileNotFoundError):
        detail = "required system command was not found"
    return f"Couldn't {action}: {detail or exc}"


def handle_command(query: str) -> str | None:
    text = query.lower()

    try:
        if "shutdown abort" in text or "cancel shutdown" in text:
            _run_command(["shutdown", "-c"])
            return "Shutdown cancelled."

        if "lock" in text and ("pc" in text or "screen" in text):
            _run_command(["loginctl", "lock-session"])
            return "Locking your PC."

        if "shutdown" in text or "shut down" in text:
            _run_command(["shutdown", "-h", "+1"])
            return "Shutting down in 1 minute. Say 'shutdown abort' to cancel."

        if "sleep" in text and ("pc" in text or "mode" in text):
            _run_command(["systemctl", "suspend"])
            return "Going to sleep."
    except (OSError, subprocess.SubprocessError) as exc:
        return _error_message("perform that power action", exc)

    return None
