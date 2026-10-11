"""Wikipedia lookup commands."""

from __future__ import annotations


def handle_command(query: str) -> str | None:
    """Return a short summary for matching Wikipedia queries."""
    topic = None
    for trigger in ("who is ", "what is ", "wikipedia ", "tell me about "):
        if trigger in query:
            topic = query.split(trigger, 1)[1].strip()
            break
    if not topic:
        return None

    try:
        import wikipedia
    except ImportError:
        return "Wikipedia lookup requires the wikipedia package."

    topic = " ".join(part for part in topic.split() if part.lower() not in {"the", "a", "an"})
    if not topic:
        return "I couldn't find a topic to look up."

    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as exc:
        options = ", ".join(exc.options[:3])
        return f"Multiple matches: {options}"
    except wikipedia.exceptions.PageError:
        return f"Sorry, no Wikipedia page for {topic}."
    except Exception as exc:  # pragma: no cover - runtime external dependency
        return f"Wikipedia error: {exc}"
