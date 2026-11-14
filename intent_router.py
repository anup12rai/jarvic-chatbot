
from ai_brain import understand_message, generate_answer
from chatbot import chatbot_response
from hardware import execute_command
from memory import get_history, add_message


def route_message(message):

    decision = understand_message(message)

    intent = decision.get("intent")
    actions = decision.get("actions", [])
    chat_message = decision.get("chat_message", "")

    if intent not in ["chat", "hardware", "mixed"]:
        return "JARVIC could not understand the request."

    if intent == "chat":
        return chatbot_response(message)

    if not isinstance(actions, list):
        return "Invalid hardware instructions."

    if intent == "hardware" and not actions:
        return chat_message or "Please clarify your hardware command."

    if intent == "mixed" and not actions:
        return chatbot_response(message)

    # Validate every action before executing any.
    allowed_devices = {
        "bedroom_light",
        "living_room_light",
        "fan"
    }

    allowed_actions = {
        "turn_on",
        "turn_off",
        "get_status"
    }

    for action in actions:
        if not isinstance(action, dict):
            return "Invalid hardware command."

        if action.get("device") not in allowed_devices:
            return "JARVIC: Unknown device. No commands executed."

        if action.get("action") not in allowed_actions:
            return "JARVIC: Invalid action. No commands executed."

    results = []

    for action in actions:
        results.append(execute_command(action))

    history = get_history()

    answer = generate_answer(
        message,
        history=history,
        hardware_results=results
    )

    add_message("user", message)
    add_message("assistant", answer)

    return answer
