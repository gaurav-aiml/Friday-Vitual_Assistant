"""Volume and brightness controls for Windows 11."""

from __future__ import annotations

import re
import subprocess


def _run_powershell(command: str) -> str:
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _get_volume() -> int:
    output = _run_powershell(
        "(Get-CimInstance -Namespace root/StandardCimv2 -ClassName CIM_AudioVolume | Select-Object -First 1).CurrentVolume"
    )
    if not output:
        raise RuntimeError("Windows 11 audio API returned an empty volume value.")
    return int(output)


def _set_volume(level: int) -> None:
    level = max(0, min(100, level))
    _run_powershell(
        f"$volume = Get-CimInstance -Namespace root/StandardCimv2 -ClassName CIM_AudioVolume | Select-Object -First 1; $volume.SetVolume({level})"
    )


def _get_brightness() -> int:
    output = _run_powershell(
        "(Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness | Select-Object -First 1).CurrentBrightness"
    )
    if not output:
        raise RuntimeError("Windows 11 brightness API returned an empty value.")
    return int(output)


def _set_brightness(level: int) -> None:
    level = max(0, min(100, level))
    _run_powershell(
        f"$brightness = Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods | Select-Object -First 1; $brightness.WmiSetBrightness(1, {level})"
    )


def _format_error(feature: str, exc: Exception) -> str:
    if isinstance(exc, FileNotFoundError):
        if feature == "volume":
            return "Windows 11 audio controls require PowerShell and an active audio device."
        return "Windows 11 brightness controls require WMI support and a compatible display."

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
        except (
            ImportError,
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
            ImportError,
            OSError,
            RuntimeError,
            subprocess.SubprocessError,
            ValueError,
        ) as exc:
            return _format_error("brightness", exc)

    return None
