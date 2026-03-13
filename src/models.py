from collections import UserDict
from datetime import date, timedelta


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

    def __str__(self):
        return f"Title: {self.title}\n Content: {self.content}"


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

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

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
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
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        return upcoming
    

class NoteBook(UserDict):
    def add_note(self, note: Note):
        self.data[note.title] = note


