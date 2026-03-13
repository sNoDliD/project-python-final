import functools

from src.models import AddressBook, Record, ValidationError, Note


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

def add_note(args, book):
    if "|" not in args:
        return "Please use format Title | Content"
    
    title, content = args.split("|", 1)
    new_note = Note(title.strip(), content.strip())
    book.add_note(new_note)

    return "Note is succesfully created"

def find_note(args, book):
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
    
def show_all_notes(args, book):
    titles = book.get_all_titles()

    if not titles:
        return "Your notebook is empty"
    
    result = "The list of your notes:\n"

    for index, title in enumerate(titles, start=1):
        result += f"{index}. {title}\n"
    
    return result.strip()

def show_note(args, book):
    if not args:
        return "Please enter the title of the note"
    
    title = args.strip().lower()
    
    found_notes = book.find_notes(title)
    
    for note in found_notes:
        if note.title.lower() == title:
            return note 
            
    return f"Note '{title}' not found"
