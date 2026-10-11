"""Volume and brightness controls."""

from __future__ import annotations

import platform


def _get_windows_volume() -> float:
    try:
        from ctypes import POINTER, cast
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return float(volume.GetMasterVolumeLevelScalar() * 100)
    except ImportError:
        return 0.0


def _set_windows_volume(level: int) -> None:
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100, None)


def _get_brightness() -> int:
    try:
        import screen_brightness_control as sbc

        return int(sbc.get_brightness()[0])
    except ImportError:
        return 0


def _set_brightness(level: int) -> None:
    try:
        import screen_brightness_control as sbc

        sbc.set_brightness(level)
    except ImportError:
        return None


def _get_volume() -> int:
    if platform.system() == "Windows":
        return int(_get_windows_volume())
    return 0


def _set_volume(level: int) -> None:
    if platform.system() == "Windows":
        _set_windows_volume(level)
    else:
        try:
            import os

            os.system(f"osascript -e 'set volume output volume {level}'")
        except Exception:
            return None


def handle_command(query: str) -> str | None:
    text = query.lower()

    if "volume" in text:
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

        level = next((int(token) for token in text.split() if token.isdigit()), None)
        if level is not None:
            _set_volume(level)
            return f"Volume set to {level}%"

    if "brightness" in text:
        current = _get_brightness()
        if "up" in text:
            new_level = min(100, current + 10)
            _set_brightness(new_level)
            return f"Brightness at {new_level}%"
        if "down" in text:
            new_level = max(0, current - 10)
            _set_brightness(new_level)
            return f"Brightness at {new_level}%"

        level = next((int(token) for token in text.split() if token.isdigit()), None)
        if level is not None:
            _set_brightness(level)
            current = _get_brightness()
            return f"Brightness at {current}%"

    return None
