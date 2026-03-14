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


def add_contact(args, book: AddressBook) -> str:
    try:
        name, phone, email, birthday, *_ = args.split(" ")
    except ValueError:
        return "Unexpected format. Please enter: <name> <phone> <email> <birthday>"
    record = book.find(name)
    created = False
    if record is None:
        record = Record(name)
        created = True

    record.set_birthday(birthday)
    if email:
        record.add_email(email)
    if phone:
        record.add_phone(phone)
    if created:
        book.add_record(record)
    return "Contact added." if created else "Contact updated."


def search_contacts(args: str, book: AddressBook):
    results = book.search(args)
    if not results:
        return "No contacts found."

    return "\n".join(str(contact) for contact in results)


def get_upcoming_birthdays(args: str, book: AddressBook):
    try:
        days = int(args)
    except ValueError:
        return f"Expect an integer, not {args!r}"

    birthdays = book.get_upcoming_birthdays(days)
    if not birthdays:
        return "No upcoming birthdays."

    return "\n".join(f"{b['name']} - {b['congratulation_date']}" for b in birthdays)


def add_note(args: str, book: NoteBook):
    if "|" not in args:
        return "Please use format Title | Content"

    title, content = args.split("|", 1)
    new_note = Note(title.strip(), content.strip())
    book.add_note(new_note)

    return "Note is successfully created"


def add_note_tags(args: str, book: NoteBook):
    try:
        note_title, *tags = args.split(" ")
    except ValueError:
        return "Unexpected format. Please enter: <note> <tag1> <tag2> ..."
    try:
        note = book[note_title]
    except KeyError:
        return f"Note with title {note_title!r} not found"
    note.tags.update(tags)
    return "Note's tags is successfully updated"


def find_note(args: str, book: NoteBook):
    if not args:
        return "Please enter search request"

    search_request = args.strip()
    found_notes = book.find_notes(search_request)

    if not found_notes:
        return f"Note for {search_request} not found"

    result = "Found notes:\n"

    for note in found_notes:
        result += f"\n{note}\n"

    return result.strip()


def show_all_notes(book: NoteBook):
    titles = book.get_all_titles()

    if not titles:
        return "Your notebook is empty"

    result = "The list of your notes:\n"

    for index, title in enumerate(titles, start=1):
        result += f"{index}. {title}\n"

    return result.strip()


def show_note(args: str, book: NoteBook):
    if not args:
        return "Please enter the title of the note"

    title = args.strip().lower()

    found_notes = book.find_notes(title)

    for note in found_notes:
        if note.title.lower() == title:
            return note

    return f"Note '{title}' not found"


def delete_note(args, book: NoteBook):
    if not args:
        return "Please enter the title of the note"
    
    title = args.strip()

    if book.delete_note(title):
        return f"Note {title} deleted"
    
    return f"Note {title} not found"


def edit_note_content(args, book: NoteBook):
    if "|" not in args:
        return "Please use format Title | New content"

    title, new_content = args.split("|", 1)

    if book.edit_note_content(title.strip(), new_content.strip()):
        return f"Content of note {title} was updated"
    else:
        return f"Note {title} not found"
    
    
def edit_note_title(args, book: NoteBook):
    if "|" not in args:
        return "Please use format Old title | New title"
    
    old_title, new_title = args.split("|", 1)

    if book.edit_note_title(old_title.strip(), new_title.strip()):
        return f"Note {old_title} was renamed to {new_title}"
    else:
        return f"Note {old_title} not found"
    
