"""Volume and brightness controls for Windows and Linux desktops."""

from __future__ import annotations

import platform
import re
import shutil
import subprocess
from importlib import import_module
from typing import Protocol, cast


class _AudioEndpoint(Protocol):
    def GetMasterVolumeLevelScalar(self) -> float: ...

    def SetMasterVolumeLevelScalar(
        self, level: float, event_context: object | None
    ) -> None: ...


class _AudioDevice(Protocol):
    @property
    def EndpointVolume(self) -> _AudioEndpoint: ...


def _get_windows_audio_endpoint() -> _AudioEndpoint:
    audio_utilities = getattr(import_module("pycaw.pycaw"), "AudioUtilities")
    device = cast(_AudioDevice, audio_utilities.GetSpeakers())
    return device.EndpointVolume


def _is_windows() -> bool:
    return platform.system() == "Windows"


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


def _get_linux_volume() -> tuple[int, str]:
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


def _get_windows_volume() -> int:
    endpoint = _get_windows_audio_endpoint()
    return round(endpoint.GetMasterVolumeLevelScalar() * 100)


def _get_volume() -> tuple[int, str | None]:
    if _is_windows():
        return _get_windows_volume(), None
    return _get_linux_volume()


def _set_linux_volume(level: int, command: str) -> None:
    level = max(0, min(100, level))
    if command.endswith("/wpctl") or command == "wpctl":
        _run_command([command, "set-volume", "@DEFAULT_AUDIO_SINK@", f"{level / 100:.2f}"])
    else:
        _run_command([command, "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])


def _set_windows_volume(level: int) -> None:
    endpoint = _get_windows_audio_endpoint()
    endpoint.SetMasterVolumeLevelScalar(max(0, min(100, level)) / 100, None)


def _set_volume(level: int, command: str | None) -> None:
    if _is_windows():
        _set_windows_volume(level)
    elif command is not None:
        _set_linux_volume(level, command)


def _run_powershell(script: str) -> str:
    command = _find_command("powershell.exe", "powershell")
    return _run_command(
        [command, "-NoProfile", "-NonInteractive", "-Command", script]
    )


def _get_linux_brightness() -> int:
    command = _find_command("brightnessctl")
    output = _run_command([command, "-m"])
    match = re.search(r"(\d{1,3})%(?:,|$)", output)
    if not match:
        raise RuntimeError(f"couldn't read brightness from brightnessctl: {output}")
    return int(match.group(1))


def _get_windows_brightness() -> int:
    output = _run_powershell(
        "(Get-CimInstance -Namespace root/WMI -ClassName "
        "WmiMonitorBrightness | Select-Object -First 1 "
        "-ExpandProperty CurrentBrightness)"
    )
    match = re.search(r"\b(\d{1,3})\b", output)
    if not match:
        raise RuntimeError("Windows did not report a brightness-capable display")
    return int(match.group(1))


def _get_brightness() -> int:
    if _is_windows():
        return _get_windows_brightness()
    return _get_linux_brightness()


def _set_linux_brightness(level: int) -> None:
    command = _find_command("brightnessctl")
    _run_command([command, "set", f"{max(0, min(100, level))}%"])


def _set_windows_brightness(level: int) -> None:
    level = max(0, min(100, level))
    _run_powershell(
        "Get-CimInstance -Namespace root/WMI -ClassName "
        "WmiMonitorBrightnessMethods | Select-Object -First 1 | "
        "Invoke-CimMethod -MethodName WmiSetBrightness "
        f"-Arguments @{{Timeout=1; Brightness={level}}} | Out-Null"
    )


def _set_brightness(level: int) -> None:
    if _is_windows():
        _set_windows_brightness(level)
    else:
        _set_linux_brightness(level)


def _format_error(feature: str, exc: Exception) -> str:
    if isinstance(exc, FileNotFoundError):
        if _is_windows():
            if feature == "volume":
                return "Windows volume control requires pycaw."
            return "Windows brightness control requires PowerShell and a compatible display."
        if feature == "volume":
            return "Linux volume controls require wpctl or pactl and an active audio device."
        return "Linux brightness controls require brightnessctl and a compatible display."

    if isinstance(exc, ImportError) and feature == "volume" and _is_windows():
        return "Windows volume control requires pycaw. Install it with 'pip install pycaw'."

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
            ImportError,
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
