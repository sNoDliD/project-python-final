# Project Python Final

A simple **CLI (Command Line Interface) assistant** for managing an address book.

The application allows you to store contacts and phone numbers and interact with them directly from the terminal.

---

## Features

| Implemented | Feature                                                                                   | Assistant Commands                                                 | Example                                                                                                                           |
|-------------|-------------------------------------------------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| ✅           | Add new contacts with names, addresses, phone numbers, emails, and birthdays              | `add-contact`, `show-contacts`                                     | `add-contact Dmytro 0981234567 dmytro@example.com 17.03.2003`                                                                     |
| ✅           | Search contacts by different criteria (e.g., by name)                                     | `search-contacts`                                                  | `search-contacts dmytro`, `search-contacts 0981234567`                                                                            |
| ✅           | Edit and delete contacts                                                                  | `edit-contact`, `delete-contact`                                   | `edit-contact Dmytro birthday 17.03.2004` , `delete-contact Dmytro`                                                               |
| ✅           | Show contacts that have birthdays within a specified number of days from the current date | `birthdays`                                                        | `birthdays 7`                                                                                                                     |
| ✅           | Validate phone numbers and email addresses when adding or editing contacts                | -                                                                  |                                                                                                                                   |
| ✅           | Ability to add text notes                                                                 | `add-note`, `all-notes`, `show-note`                               | `add-note Products \| milk, cheese, sausage`                                                                                      |
| ✅           | Search, edit, and delete notes                                                            | `find-note`, `edit-note-content`, `edit-note-title`, `delete-note` | `find-note Products`, `edit-note-content Products \| coffe, tea`, `edit-note-title Products \| Breakfast`, `delete-note Products` |
| ✅           | Persist all data (contacts and notes) on disk in the user directory                       | -                                                                  |                                                                                                                                   |
| ✅           | Restart the assistant without losing data                                                 | -                                                                  |                                                                                                                                   |
| ✅           | Add tags to notes                                                                         | `add-tags`                                                         | `add-tags Products buy-list shoping`                                                                                              |
| ✅           | Search and sort notes by tags                                                             | `find-tag`, `sort-tag`                                             | `find-tag shoping`, `sort-tag buy-list`                                                                                           |

- ❌ - not implemented
- 🔀 - in progress
- ✅ - done

---

## Prerequisites

Before running the project make sure that the following software is installed:

- **Python 3.10+**
- **Git**

Check Python installation:

`python3 --version` or `python --version`

---

## Installation

### 1. Clone the repository

``` shell
git clone <REPOSITORY_URL>
```

### 2. Navigate to the project directory

``` shell
cd project-python-final
```

### 3.1 Run the application from source

`python3 main.py` or `python main.py`

### 3.2 Run the application as package

1. `pip install .`
2. `assistant-bot`

---

## CLI Usage Example

Example of working with the assistant in the terminal:

```
$ python main.py

Welcome to the assistant bot!
Enter a command: add-contact Dmytro 0981234567 dmytro@example.com 17.03.2003
Contact added.

Enter a command: add-contact Dmytro 0987654321 dmytro-extra@example.com 17.03.2003
Contact updated.

Enter a command: show-contacts
Contact name: Dmytro, phones: 0987654321; 0981234567, emails: dmytro-extra@example.com; dmytro@example.com, birthday: 17.03.2003

Enter a command: exit
Good bye!
```

---

## Project Structure

```
project-python-final
│
├── main.py
├── README.md
│
└── src
    ├── assistant.py
    ├── handlers.py
    └── models.py
```
