import functools

from src.models import AddressBook, Record, ValidationError, Note, NoteBook


def handle_error(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValidationError,) as e:
            return str(e)
        except (ValueError, IndexError):
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."

    return inner


def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())


def add_contact(args: str, book: AddressBook) -> str:
    name, phone, *_ = args.split(" ")
    record = book.find(name)
    created = False
    if record is None:
        record = Record(name)
        created = True

    if phone:
        record.add_phone(phone)
    if created:
        book.add_record(record)
    return "Contact added." if created else "Contact updated."


def add_note(args: str, book: NoteBook):
    if "|" not in args:
        return "Please use format Title | Content"

    title, content = args.split("|", 1)
    new_note = Note(title.strip(), content.strip())
    book.add_note(new_note)

    return "Note is successfully created"
