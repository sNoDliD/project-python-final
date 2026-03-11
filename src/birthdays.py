from datetime import date, timedelta


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
