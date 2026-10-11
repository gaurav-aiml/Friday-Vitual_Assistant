"""Battery status reporting."""

from __future__ import annotations


def handle_command(query: str) -> str | None:
    if "battery" not in query:
        return None

    try:
        import psutil
    except ImportError:
        return "Battery status requires psutil."

    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected — desktop PC."

    status = "plugged in" if battery.power_plugged else "on battery"
    return f"Battery at {int(battery.percent)} percent, {status}."
