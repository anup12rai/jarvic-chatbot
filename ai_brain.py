
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


def understand_message(message):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
                You are JARVIC's intent detection engine.

                Understand the complete user request.

                Return JSON in this format:

                {
                    "intent": "chat",
                    "chat_message": "",
                    "actions": []
                }

                Available intents:
                chat, hardware, mixed.

                Available devices:
                bedroom_light,
                living_room_light,
                fan.

                Available actions:
                turn_on, turn_off, get_status.

                Rules:
                - Normal questions are chat.
                - Device commands are hardware.
                - Questions combined with device commands are mixed.
                - Never invent devices or actions.
                - If a device is unclear, ask for clarification.
                - Do not create hardware actions when unclear.
                """
            },
            {
                "role": "user",
                "content": message
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    return json.loads(
        response.choices[0].message.content
    )


def generate_answer(message, history=None, hardware_results=None):

    messages = [
        {
            "role": "system",
            "content": """
            You are JARVIC, a friendly and intelligent AI assistant.

            Answer naturally and clearly.
            Understand conversation context.
            Explain technical concepts.

            When hardware results are provided:
            - Report only confirmed results.
            - Never pretend a failed command succeeded.
            - Explain pending or unavailable devices honestly.
            """
        }
    ]

    messages.extend(history or [])

    context = {
        "user_message": message,
        "hardware_results": hardware_results or []
    }

    messages.append({
        "role": "user",
        "content": json.dumps(context)
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content
