# Project Python Final

A simple **CLI (Command Line Interface) assistant** for managing an address book.

The application allows you to store contacts and phone numbers and interact with them directly from the terminal.

---

## Features

| Implemented | Feature                                                                                   | Assistant Commands                        |
|-------------|-------------------------------------------------------------------------------------------|-------------------------------------------|
| 🔀          | Add new contacts with names, addresses, phone numbers, emails, and birthdays              | `add`                                     |
| ❌           | Search contacts by different criteria (e.g., by name)                                     | `search`                                  |
| ❌           | Edit and delete contacts                                                                  | `edit`, `delete`                          |
| ❌           | Show contacts that have birthdays within a specified number of days from the current date | `birthdays`                               |
| 🔀          | Validate phone numbers and email addresses when adding or editing contacts                | `add`, `edit`                             |
| ❌           | Ability to add text notes                                                                 | `note-add`                                |
| ❌           | Search, edit, and delete notes                                                            | `note-search`, `note-edit`, `note-delete` |
| ❌           | Persist all data (contacts and notes) on disk in the user directory                       | `save`, `load`                            |
| ❌           | Restart the assistant without losing data                                                 | `save`, `load`                            |
| ❌           | Add tags to notes                                                                         | `tag-add`                                 |
| ❌           | Search and sort notes by tags                                                             | `tag-search`, `tag-sort`                  |

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

### 3. Run the application

`python3 main.py` or `python main.py`

---

## Available Commands

| Command              | Description                                 |
|----------------------|---------------------------------------------|
| `add <name> <phone>` | Add a new contact or update an existing one |
| `show`               | Display all saved contacts                  |
| `exit` / `close`     | Exit the assistant                          |

---

## CLI Usage Example

Example of working with the assistant in the terminal:

```
$ python main.py

Welcome to the assistant bot!
Enter a command: add John 123456789
Contact added.

Enter a command: add John 987654321
Contact updated.

Enter a command: show
John: 123456789, 987654321

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
