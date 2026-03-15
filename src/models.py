import pickle
import re
import typing
from collections import UserDict
from datetime import date, timedelta, datetime
from pathlib import Path

HOME_DIR = Path.home()


class ValidationError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValidationError("Name is required")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValidationError(f"Phone number must contain exactly 10 digits: {value!r}")
        super().__init__(value)


class Email(Field):
    pattern = re.compile(r'([A-Za-z0-9]+[._-])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    def __init__(self, value: str):
        if not re.fullmatch(self.pattern, value):
            raise ValidationError(f"Invalid email format: {value!r}")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            _date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.tags: typing.Set[str] = set()

    def __str__(self):
        title = f"Title: {self.title}"
        if tags := self.tags:
            title += f" [{', '.join(tags)}]"
        return f"{title}\n Content: {self.content}"


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: typing.List[Phone] = []
        self.emails: typing.List[Email] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def add_email(self, email: str):
        self.emails.append(Email(email))

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValidationError("Phone not found")
        self.phones.remove(phone_obj)
        self.phones.append(Phone(new_phone))

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def set_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        info = [f"Contact name: {self.name.value}"]
        if phones := self.phones:
            info.append(f"phones: {'; '.join(str(i) for i in phones)}")
        if emails := self.emails:
            info.append(f"emails: {'; '.join(str(i) for i in emails)}")
        if birthday := self.birthday:
            info.append(f"birthday: {birthday}")
        return ", ".join(info)


class PickleDumper:
    dump_filepath: str

    def dump(self):
        with open(self.dump_filepath, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls):
        try:
            with open(cls.dump_filepath, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()


class AddressBook(PickleDumper, UserDict):
    dump_filepath = HOME_DIR / "addressbook.pickle"

    def add_record(self, record: Record):
        self[record.name.value] = record

    def find(self, name: str) -> "Record | None":
        return self.get(name)

    def delete(self, name: str):
        self.pop(name, None)

    def search(self, query: str):
        query = query.lower()
        result = []

        for record in self.values():
            if query in record.name.value.lower():
                result.append(record)
                continue

            for phone in record.phones:
                if query in phone.value:
                    result.append(record)
                    break

        return result

    @staticmethod
    def _get_birthday_date(birthday: date, year: int) -> date:
        try:
            return birthday.replace(year=year)
        except ValidationError:
            return date(year, 3, 1)

    def get_upcoming_birthdays(self, days: int):
        today = date.today()
        upcoming = []

        for record in self.values():
            if not record.birthday:
                continue

            birthday_this_year = self._get_birthday_date(record.birthday.value, today.year)

            if birthday_this_year < today:
                nearest_birthday = self._get_birthday_date(record.birthday.value, today.year + 1)
            else:
                nearest_birthday = birthday_this_year

            delta_days = (nearest_birthday - today).days

            if 0 <= delta_days <= days:
                congratulation_date = nearest_birthday

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })
        return upcoming


class NoteBook(PickleDumper, UserDict):
    dump_filepath = HOME_DIR / "notebook.pickle"

    def add_note(self, note: Note):
        self.data[note.title] = note

    def find_notes(self, search_text: str):
        search_request = search_text.lower()
        found_notes = []

        for title, note in self.data.items():
            if search_request in title.lower() or search_request in note.content.lower():
                found_notes.append(note)

        return found_notes

    def get_all_titles(self):
        if not self.data:
            return []

        return list(self.data.keys())

    def delete_note(self, title: str):
        if title in self.data:
            del self.data[title]
            return True

        return False

    def edit_note_content(self, title: str, new_content: str):
        if title in self.data:
            self.data[title].content = new_content
            return True

        return False

    def edit_note_title(self, old_title: str, new_title: str):
        if old_title in self.data:
            content = self.data[old_title].content
            new_note = Note(new_title, content)
            self.add_note(new_note)
            self.delete_note(old_title)
            return True

        return False

    def find_note_by_tag(self, tag: str):
        search_tag = tag.strip().lower()
        found_notes = []

        for note in self.data.values():
            if search_tag in note.tags:
                found_notes.append(note)

        return found_notes

    def sort_notes_by_tag(self, tag: str):
        search_tag = tag.strip().lower()

        filtered_notes = [
            note for note in self.data.values()
            if search_tag in [t.lower() for t in note.tags]
        ]

        return sorted(filtered_notes, key=lambda x: x.title.lower())
