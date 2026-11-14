
import json
import os

MEMORY_FILE = "jarvic_memory.json"
MAX_MESSAGES = 30


def get_history():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (OSError, json.JSONDecodeError):
        return []


def add_message(role, content):
    history = get_history()

    history.append({
        "role": role,
        "content": content
    })

    history = history[-MAX_MESSAGES:]

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def clear_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)
