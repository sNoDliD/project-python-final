import typing

from src import handlers
from src.handlers import handle_error
from src.models import AddressBook, NoteBook


class Assistant:
    def __init__(self):
        self.book = self._load_address_book()
        self.notes = NoteBook()
        self.alive = True

    @staticmethod
    def _load_address_book() -> AddressBook:
        return AddressBook()

    @classmethod
    def show_welcome_message(cls) -> None:
        cls.show_message("Welcome to the assistant bot!")

    @staticmethod
    def show_message(text: str) -> None:
        print(text)

    @staticmethod
    def wait_command() -> typing.Tuple[str, str]:
        user_input = input("Enter a command: ")
        cmd, _, args = user_input.strip().partition(" ")
        return cmd.lower(), args.strip()

    @handle_error
    def handle(self, command: str, args: str) -> str:
        if command in ["close", "exit"]:
            self.alive = False
            return "Good bye!"
        elif command == "show":
            return handlers.show_all(self.book)
        elif command == "add":
            return handlers.add_contact(args, self.book)
        elif command == "search":
            results = self.book.search(args)

            if not results:
                return "No contacts found."

            return "\n".join(str(contact) for contact in results)
        elif command == "birthdays":
            birthdays = self.book.get_upcoming_birthdays(int(args))

            if not birthdays:
                return "No upcoming birthdays."

            return "\n".join(f"{b['name']} - {b['congratulation_date']}" for b in birthdays)
        elif command == "add-note":
            return handlers.add_note(args, self.notes)
        elif command == "find-note":
            return handlers.find_note(args, self.notes)
        elif command == "all-notes":
            return handlers.show_all_notes(args, self.notes)
        elif command == "show-note":
            return handlers.show_note(args, self.notes)

        return "Unknown command."
