"""Volume and brightness controls."""

from __future__ import annotations

import re
import subprocess


def _get_volume() -> int:
    result = subprocess.run(
        ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.search(r"/\s*(\d+)%", result.stdout)
    if match is None:
        raise RuntimeError("pactl returned an unrecognized volume value.")
    return int(match.group(1))


def _set_volume(level: int) -> None:
    subprocess.run(
        ["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"],
        check=True,
        capture_output=True,
        text=True,
    )


def _get_brightness() -> int:
    result = subprocess.run(
        ["brightnessctl", "get"],
        check=True,
        capture_output=True,
        text=True,
    )
    maximum = subprocess.run(
        ["brightnessctl", "max"],
        check=True,
        capture_output=True,
        text=True,
    )
    current_value = int(result.stdout.strip())
    maximum_value = int(maximum.stdout.strip())
    if maximum_value <= 0:
        raise RuntimeError("brightnessctl reported an invalid maximum.")
    return round(current_value * 100 / maximum_value)


def _set_brightness(level: int) -> None:
    level = max(0, min(100, level))
    subprocess.run(
        ["brightnessctl", "set", f"{level}%"],
        check=True,
        capture_output=True,
        text=True,
    )


def _format_error(feature: str, exc: Exception) -> str:
    if isinstance(exc, FileNotFoundError):
        if feature == "volume":
            return "Volume control requires pactl; install pulseaudio-utils and ensure audio is running."
        return "Brightness control requires brightnessctl; install it and check display permissions."

    detail = getattr(exc, "stderr", None)
    if detail:
        detail = detail.strip()
    return f"Couldn't control {feature}: {detail or exc}"


def handle_command(query: str) -> str | None:
    text = query.lower()

    if "volume" in text:
        try:
            if "up" in text:
                new_level = min(100, _get_volume() + 10)
                _set_volume(new_level)
                return f"Volume at {new_level}%"
            if "down" in text:
                new_level = max(0, _get_volume() - 10)
                _set_volume(new_level)
                return f"Volume at {new_level}%"
            if "mute" in text:
                _set_volume(0)
                return "Muted"

            level = next(
                (int(token) for token in text.split() if token.isdigit()), None
            )
            if level is not None:
                level = max(0, min(100, level))
                _set_volume(level)
                return f"Volume set to {level}%"
        except (ImportError, OSError, RuntimeError, subprocess.SubprocessError, ValueError) as exc:
            return _format_error("volume", exc)

    if "brightness" in text:
        try:
            current = _get_brightness()
            if "up" in text:
                new_level = min(100, current + 10)
                _set_brightness(new_level)
                return f"Brightness at {new_level}%"
            if "down" in text:
                new_level = max(0, current - 10)
                _set_brightness(new_level)
                return f"Brightness at {new_level}%"

            level = next(
                (int(token) for token in text.split() if token.isdigit()), None
            )
            if level is not None:
                _set_brightness(level)
                current = _get_brightness()
                return f"Brightness at {current}%"
        except (ImportError, OSError, RuntimeError, subprocess.SubprocessError, ValueError) as exc:
            return _format_error("brightness", exc)

    return None
