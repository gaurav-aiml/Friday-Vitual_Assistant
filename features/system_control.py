"""Volume and brightness controls for Linux desktops."""

from __future__ import annotations

import re
import shutil
import subprocess


def _find_command(*candidates: str) -> str:
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError(f"none of {', '.join(candidates)} is installed")


def _run_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _get_volume() -> tuple[int, str]:
    command = _find_command("wpctl", "pactl")
    if command.endswith("/wpctl") or command == "wpctl":
        output = _run_command([command, "get-volume", "@DEFAULT_AUDIO_SINK@"])
        match = re.search(r"Volume:\s*([\d.]+)", output)
        if not match:
            raise RuntimeError(f"couldn't read volume from wpctl: {output}")
        return round(float(match.group(1)) * 100), command

    output = _run_command([command, "get-sink-volume", "@DEFAULT_SINK@"])
    match = re.search(r"(\d{1,3})%", output)
    if not match:
        raise RuntimeError(f"couldn't read volume from pactl: {output}")
    return int(match.group(1)), command


def _set_volume(level: int, command: str) -> None:
    level = max(0, min(100, level))
    if command.endswith("/wpctl") or command == "wpctl":
        _run_command([command, "set-volume", "@DEFAULT_AUDIO_SINK@", f"{level / 100:.2f}"])
    else:
        _run_command([command, "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])


def _get_brightness() -> int:
    command = _find_command("brightnessctl")
    output = _run_command([command, "-m"])
    match = re.search(r"(\d{1,3})%(?:,|$)", output)
    if not match:
        raise RuntimeError(f"couldn't read brightness from brightnessctl: {output}")
    return int(match.group(1))


def _set_brightness(level: int) -> None:
    command = _find_command("brightnessctl")
    _run_command([command, "set", f"{max(0, min(100, level))}%"])


def _format_error(feature: str, exc: Exception) -> str:
    if isinstance(exc, FileNotFoundError):
        if feature == "volume":
            return "Linux volume controls require wpctl or pactl and an active audio device."
        return "Linux brightness controls require brightnessctl and a compatible display."

    detail = getattr(exc, "stderr", None)
    if detail:
        detail = detail.strip()
    return f"Couldn't control {feature}: {detail or exc}"


def handle_command(query: str) -> str | None:
    text = query.lower()

    if "volume" in text:
        try:
            current, command = _get_volume()
            if "up" in text:
                new_level = min(100, current + 10)
                _set_volume(new_level, command)
                return f"Volume at {new_level}%"
            if "down" in text:
                new_level = max(0, current - 10)
                _set_volume(new_level, command)
                return f"Volume at {new_level}%"
            if "mute" in text:
                _set_volume(0, command)
                return "Muted"

            level = next(
                (int(token) for token in text.split() if token.isdigit()), None
            )
            if level is not None:
                level = max(0, min(100, level))
                _set_volume(level, command)
                return f"Volume set to {level}%"
        except (
            OSError,
            RuntimeError,
            subprocess.SubprocessError,
            ValueError,
        ) as exc:
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
        except (
            OSError,
            RuntimeError,
            subprocess.SubprocessError,
            ValueError,
        ) as exc:
            return _format_error("brightness", exc)

    return None
