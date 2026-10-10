import webbrowser


def handle_command(query: str) -> None:
    query = query.lower()

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
