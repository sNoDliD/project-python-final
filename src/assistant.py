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
        elif command == "show-contacts":
            return handlers.show_all(self.book)
        elif command == "add-contact":
            return handlers.add_contact(args, self.book)
        elif command == "search-contacts":
            return handlers.search_contacts(args, self.book)
        elif command == "birthdays":
            return handlers.get_upcoming_birthdays(args, self.book)
        elif command == "add-note":
            return handlers.add_note(args, self.notes)
        elif command == "add-tags":
            return handlers.add_note_tags(args, self.notes)
        elif command == "find-note":
            return handlers.find_note(args, self.notes)
        elif command == "all-notes":
            return handlers.show_all_notes(self.notes)
        elif command == "show-note":
            return handlers.show_note(args, self.notes)
        elif command == "delete-note":
            return handlers.delete_note(args, self.notes)
        elif command == "edit-note-content":
            return handlers.edit_note_content(args, self.notes)
        elif command == "edit-note-title":
            return handlers.edit_note_title(args, self.notes)
        elif command == "find-tag":
            return handlers.find_notes_by_tag(args, self.notes)
        elif command == "sort-tag":
            return handlers.sort_by_tag(args, self.notes)

        return "Unknown command."
