from src.assistant import Assistant


def main():
    assistant = Assistant()
    assistant.show_welcome_message()

    while assistant.alive:
        command, args = assistant.wait_command()
        if message := assistant.handle(command, args):
            assistant.show_message(message)


if __name__ == "__main__":
    main()
