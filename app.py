
from dotenv import load_dotenv
load_dotenv()

from intent_router import route_message
from memory import clear_memory
from hardware import get_all_devices


def main():

    print("\n================================")
    print("       JARVIC AI ONLINE")
    print("================================")

    print("Llama + Groq connected")
    print("Chatbot: Ready")
    print("Hardware simulator: Ready")
    print("Memory: Enabled")

    print("\nCommands:")
    print("  /devices - Show device status")
    print("  /clear   - Clear conversation memory")
    print("  exit     - Close JARVIC")

    while True:

        try:
            message = input("\nYou: ").strip()

            if not message:
                continue

            if message.lower() in ["exit", "quit"]:
                print("JARVIC: Goodbye!")
                break

            if message.lower() == "/clear":
                clear_memory()
                print("JARVIC: Conversation memory cleared.")
                continue

            if message.lower() == "/devices":
                print("JARVIC:", get_all_devices())
                continue

            answer = route_message(message)

            print("\nJARVIC:", answer)

        except KeyboardInterrupt:
            print("\nJARVIC: Shutting down.")
            break

        except Exception as error:
            print("\nJARVIC error:", error)


if __name__ == "__main__":
    main()
