import webbrowser

from features import (
    app_launcher,
    battery,
    clipboard_tool,
    power_control,
    screenshot,
    system_control,
    whatsapp,
    wikipedia_tool,
)

from storage import todos


def handle_command(query: str) -> str | None:
    query = query.lower().strip()
    if not query:
        return None

    if query.startswith("add task "):
        task = query.replace("add task ", "", 1).strip()
        return todos.add_task(task)

    if query.startswith(("complete task ", "done task ", "finish task ")):
        try:
            task_id = int(query.split()[-1])
            return todos.complete_task(task_id)
        except ValueError:
            return "Please say the task number."

    if "clear" in query and "task" in query:
        return todos.clear_done()

    if ("task" in query or "todo" in query) and any(
        word in query for word in ("show", "list", "my", "what")
    ):
        return todos.list_tasks()

    for module in (
        whatsapp,
        clipboard_tool,
        power_control,
        screenshot,
        system_control,
        battery,
        wikipedia_tool,
        app_launcher,
    ):
        response = module.handle_command(query)
        if response:
            return response

    if "open browser" in query:
        webbrowser.open("https://www.google.com")
        return "Opening browser."
    if "open linkedin" in query:
        webbrowser.open("https://www.linkedin.com/in/gauravaiml")
        return "Opening LinkedIn."
    if "open github" in query:
        webbrowser.open("https://www.github.com/gaurav-aiml")
        return "Opening GitHub."
    if "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    if "open my channel" in query:
        webbrowser.open("https://www.youtube.com/@gaurav-aiml")
        return "Opening your channel."

    return "I didn't catch that, Sir."
