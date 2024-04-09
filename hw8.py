from collections import UserDict
from datetime import datetime , timedelta
import pickle
#Сереалізація 
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  
#Основні класи
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Ім\'я обов\'язкове")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self._validate_phone(value):
            return "Неправильний формат номера"
        super().__init__(value)

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value= datetime.strptime(value,'%d.%m.%Y')
        except ValueError:
            return "Invalid date format. Use DD.MM.YYYY"



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def return_name(self):
        return self.name

    def add_phone(self, phone):
            self.phones.append( Phone(phone))


    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
    
    def edit_phone(self, old_num, new_num):
        if self.find_phone(old_num):
            self.add_phone(new_num)
            self.remove_phone(old_num)
        else: 
            raise ValueError ("Такого номера не існує")
    
    def find_phone(self,number):
         for phone in self.phones:
              if phone.value == number:
                   return phone 
              else: raise ValueError ("Такого номера не існує")

    
    def add_birthday(self,birthday):
        self.birthday = Birthday(birthday)
    

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value.strftime("%d.%m.%Y")}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record:Record):
          self.data[record.name.value] = record

    def find(self, name):
         return self.data.get(name)
    
    def delete(self, name):
         if name in self.data:
              del self.data[name]

    def get_upcoming_birthdays(self):
        prepared_users = []
        for record in self.data.values():
            if record.birthday.value: 
                prepared_users.append({"name": record.name.value, "birthday":record.birthday.value.date()})

        today=datetime.today().date()
        days = 7
        def find_next_weekday(d , weekday: int):
            days_ahead =weekday -d.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return d + timedelta(days=days_ahead)
        upcoming_birthdays= ""
        for kolega in prepared_users: 
            this_year_birth = kolega['birthday'].replace(year=today.year)
            if this_year_birth < today:
                this_year_birth = this_year_birth.replace(year=today.year +1)
            if 0 <= (this_year_birth- today).days <= days:
                if this_year_birth.weekday() >= 5:
                    this_year_birth = find_next_weekday(this_year_birth, 0)
                congratulation = this_year_birth.strftime("%Y.%m.%d")
                upcoming_birthdays=upcoming_birthdays+f'name: {kolega["name"]}, congratulation_date: {congratulation}\n'
        return upcoming_birthdays
    
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())



#Декоратори

    
def input_error_add(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Gime me name and phone"
        except TypeError:
            return "The phone number length should be 10 characters."
    return inner

def input_error_change(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Gime me name,old number, and new number"
        except TypeError:
            return "The phone number length should be 10 characters."
    return inner
    

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return "Invalid command."

    return inner
def input_error_phone(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError,IndexError):
            return "Give me name please."
        except KeyError: 
            return "No contacts found."  
    return inner

def input_error_birth_add(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and birthday date"
        except TypeError:
            return "Invalid date format. Use DD.MM.YYYY"
    return inner

def input_error_birth_show(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name"
    return inner

#Внутрішні функції

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error_add
def add_contact(args, book: AddressBook):
    name, phone, = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error_change
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone, = args
    record = book.find(name)
    if record is None:
        return "Contact not found" 
    record.edit_phone(old_phone, new_phone)
    return "Contact changed."

@input_error_phone
def phone_contact(args, book: AddressBook):
    name, = args
    if not book.find(name):
        return "Contact not found"
    return book.find(name)

def show_all(book: AddressBook, args=None):
    if args:
        return "I need only command \"all\" "
    if not book:
        return "No contacts found."
    else:
        return book
@input_error_birth_add    
def add_birthday(args, book: AddressBook):
    name, birth, = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    record.add_birthday(birth)
    return "Contact updated."

@input_error_birth_show    
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    if record.birthday:
        return f"{name}\'s birthday: {record.birthday}"
    else: 
        return "Birthday not provided"
    
def birthdays(book: AddressBook, args=None):
    if args:
        return "I need only command \"birthdays\" "
    if not book:
        return "No contacts found."
    else:
        return book.get_upcoming_birthdays()
    
def help(args= None):
    if args:
        return "I need only command \"help\" "
    return """
                                    |LIST OF COMMANDS|
    ________________________________________________________________________________                              
    |\"exit\" or \"close\" to close the bot                                            |
    |\"add [name] [phone(length-10 symbols)]\" to create a new contact               |
    |\"phone [name]\" to find contact by name                                        |
    |\"change [name] [old number] [new number]\" to change contact phone             |
    |\"all\" or \"show\" to show all contacts                                          |
    |\"add-birthday [name] [birthday(format-DD.MM.YYYY)]\" to add birthday to contact|
    |\"show-birthday [name]\" to show birthday by name                               |
    |\"birthdays\" to show all birthdays in the coming week                          |
    --------------------------------------------------------------------------------
    """


    
#Головна функція

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello" or command=="hi":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "phone":
            print(phone_contact(args,book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "all" or command=="show":
            print(show_all(book, args))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book, args))
        elif command == "help":
            print(help())
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()