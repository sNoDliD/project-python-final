import functools

from src.models import AddressBook, Record, ValidationError


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


def add_contact(args, book: AddressBook) -> str:
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
