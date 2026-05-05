# Address Book — Pickle Persistence

CLI address book that survives restarts. Builds on the previous iteration by adding `pickle` serialization so contacts are saved to `addressbook.pkl` on exit and reloaded on next launch.

## Stack

- Python 3.12 (standard library only)

## Commands

| Command | Action |
|---------|--------|
| `add <name> <phone>` | Create a contact |
| `change <name> <old_phone> <new_phone>` | Update a phone |
| `phone <name>` | Show all phones for a contact |
| `add-birthday <name> <DD.MM.YYYY>` | Set the birthday |
| `show-birthday <name>` | Show one contact's birthday |
| `birthdays` | List birthdays in the next 7 days (skipping weekends) |
| `all` | List all contacts |
| `close` / `exit` | Save book and exit |
| `hello` | Greeting |

## Run

```bash
python hw8.py
```

State lives in `addressbook.pkl` next to the script.
