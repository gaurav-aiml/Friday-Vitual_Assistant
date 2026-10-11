import webbrowser

import todos


def handle_command(query: str) -> None:
    query = query.lower()
    
    if query.startswith("add task "):
        task = query.replace("add task ", "", 1).strip()
        return todos.add_task(task)
    
    if query.startswith(("complete task ", "done task ", "finish task ")):
        try:
            tid = int(query.split()[-1])
            return todos.complete_task(tid)
        except ValueError:
            return "Please say the task number."
        
    if "clear" in query and "task" in query:
        return todos.clear_done()

    if ("task" in query or "todo" in query) and any(
        w in query for w in ["show", "list", "my", "what"]
    ):
        return todos.list_tasks()

    if "open browser" in query:
        webbrowser.open("https://www.google.com")
    elif "open linkedin" in query:
        webbrowser.open("https://www.linkedin.com/in/gauravaiml")
    elif "open github" in query:
        webbrowser.open("https://www.github.com/gaurav-aiml")
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
    elif "open my channel" in query:
        webbrowser.open("https://www.youtube.com/@gaurav-aiml")
