"""WhatsApp message sending helper."""

from __future__ import annotations

import re

CONTACTS = {
    "mom": "+919999999999",
    "dad": "+918888888888",
    "rahul": "+917777777777",
}


def handle_command(query: str) -> str | None:
    if "whatsapp" not in query:
        return None

    match = re.search(r"to\s+(\w+).*?(?:saying|that|message)\s+(.+)", query, flags=re.IGNORECASE)
    if not match:
        return "Say: send whatsapp to <name> saying <message>"

    name, message = match.group(1).lower(), match.group(2).strip()
    phone = CONTACTS.get(name)
    if not phone:
        return f"No number saved for {name}."

    try:
        import pywhatkit

        pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=True)
        return f"Message sent to {name}."
    except Exception as exc:  # pragma: no cover - depends on browser environment
        return f"WhatsApp failed: {exc}"
