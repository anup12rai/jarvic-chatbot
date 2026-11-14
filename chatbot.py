
from ai_brain import generate_answer
from memory import get_history, add_message


def chatbot_response(message):

    history = get_history()

    answer = generate_answer(
        message,
        history=history
    )

    add_message("user", message)
    add_message("assistant", answer)

    return answer
