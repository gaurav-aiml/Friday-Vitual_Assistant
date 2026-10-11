import json
import os
from datetime import datetime

TODO_FILE = "todos.json"


def _load():
    """Load todos from JSON file."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save(todos):
    """Save todos to JSON file."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def add_task(task):
    todos = _load()
    new_task = {
        "id": len(todos) + 1 if not todos else max(t["id"] for t in todos) + 1,
        "task": task,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    todos.append(new_task)
    _save(todos)
    return f"Added: '{task}'"


def list_tasks(show_done=True):
    todos = _load()
    if not todos:
        return "Your to-do list is empty."

    lines = ["📋 Your To-Do List:"]
    for t in todos:
        if not show_done and t["done"]:
            continue
        status = "✅" if t["done"] else "⬜"
        lines.append(f"  {status} [{t['id']}] {t['task']}")
    return "\n".join(lines)


def complete_task(task_id):
    todos = _load()
    for t in todos:
        if t["id"] == task_id:
            t["done"] = True
            _save(todos)
            return f"Marked '{t['task']}' as done."
    return f"No task with ID {task_id}."


def delete_task(task_id):
    todos = _load()
    new_todos = [t for t in todos if t["id"] != task_id]
    if len(new_todos) == len(todos):
        return f"No task with ID {task_id}."
    _save(new_todos)
    return f"Deleted task {task_id}."


def clear_done():
    todos = _load()
    remaining = [t for t in todos if not t["done"]]
    count = len(todos) - len(remaining)
    _save(remaining)
    return f"Cleared {count} completed task(s)."