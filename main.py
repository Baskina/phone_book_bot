from collections import UserDict
import re


class WrongPhoneFormatError(ValueError):
    pass


class EmptyPhoneNumberError(Exception):
    pass


class EmptyNameError(Exception):
    pass


class ShortNameError(Exception):
    pass


class PhoneNotExistError(ValueError):
    pass


def input_error(handler):
    def error_handler(data):
        try:
            return handler(data)
        except EmptyPhoneNumberError:
            return f'Phone is required'
        except EmptyNameError:
            return f'Name is required'
        except ShortNameError:
            return f'Name should have at lest 3 characters'
        except WrongPhoneFormatError:
            return f'Phone should have 10 decimals'
        except PhoneNotExistError:
            return 'Phone doesn\'t exist'
        except Exception as error:
            return f'Something happens: {error}'

    return error_handler


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return 'The record was added'

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)
            return f'The record {name} was deleted'
        else:
            return f'No records with {name} name'


book = AddressBook()


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.check_format(value)
        self.value = value

    def check_format(self, value):
        if not re.match(r'^(\D{3,})$', value):
            raise ShortNameError


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.check_format(value)
        self.value = value

    def check_format(self, value):
        if not re.match(r'^(\d{10})$', value):
            raise WrongPhoneFormatError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        self.phones = self.phones

    def edit_phone(self, old_phone, new_phone):
        new_phone_set = []
        if not old_phone in list(map(lambda x: x.value, self.phones)):
            raise PhoneNotExistError
        for phone in self.phones:
            if phone.value == old_phone:
                new_phone_set.append(Phone(new_phone))
            else:
                new_phone_set.append(phone)
        self.phones = new_phone_set

    def find_phone(self, phone):
        if phone in list(map(lambda x: x.value, self.phones)):
            for item in self.phones:
                if item.value == phone:
                    return item
        else:
            return None

    def remove_phone(self, phone):
        if phone in list(map(lambda x: x.value, self.phones)):
            for i, phone_item in enumerate(self.phones):
                if phone_item.value == phone:
                    del self.phones[i]
                    break
            return f"{phone} removed"
        else:
            return f'{self.name} doesn\'t have {phone} phone'

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


@input_error
def handler_add(data):
    if not data or len(data) < 1 or not data[0]:
        raise EmptyNameError
    record = Record(data[0])

    if len(data) < 2:
        raise EmptyPhoneNumberError

    for phone in data[1:]:
        record.add_phone(phone)

    book.add_record(record)
    return 'Contact is added'


@input_error
def handler_find_by_name(name):
    return book.find(name[0])


@input_error
def handler_find_phone(data):
    record = book.find(data[0])
    return record.find_phone(data[1])


@input_error
def handler_remove_phone(data):
    record = book.find(data[0])
    return record.remove_phone(data[1])


@input_error
def handler_update(data):
    record = book.find(data[0])
    record.edit_phone(data[1], data[2])
    return 'Contact updated'


@input_error
def handler_add_phone(data):
    record = book.find(data[0])
    for phone in data[1:]:
        record.add_phone(phone)
    return 'Contact updated'


def handler_show_all(*args):
    if not book:
        return 'No names in your phone book'
    contact_list = ''
    for name, value in book.data.items():
        phones = '; '.join(list(map(lambda x: x.value, value.phones)))
        contact_list += 'Name: {} --- Phones: {}\n'.format(name, phones)
    return contact_list


@input_error
def handler_delete(data):
    return book.delete(data[0])


def handler_greetings(*args):
    return 'How can I help you?'


COMMANDS_RGX = 'hello|close|exit|good bye|' \
               'add contact|' \
               'change phone|' \
               'find contact by name|' \
               'show all|' \
               'add extra phone|' \
               'find phone|' \
               'delete contact|' \
               'remove phone'

BOT_COMMANDS = 'hello\n' \
               'close\n' \
               'exit\n' \
               'good bye\n' \
               'add contact {name}(required) {phone}(required) {phone}(optional) X multiple\n' \
               'change phone {name}(r) {old phone}(r) {new phone}(r)\n' \
               'find contact by name {name}(r)\n' \
               'show all\n' \
               'add extra phone {name}(r) {new phone}(r)\n' \
               'find phone {name}(r) {phone}(r)\n' \
               'delete contact {name}(r)\n' \
               'remove phone {name}(r) {phone}(r)'


def parser(line):
    data_array = list(filter(None, re.split(COMMANDS_RGX, line)))
    command = re.search(COMMANDS_RGX, line)

    data = data_array[0].strip().split(' ') if len(data_array) > 0 else None
    return command.group(), data


def get_handler(operator):
    return OPERATORS[operator]


is_listening = True


def handler_bye(*args):
    global is_listening
    is_listening = False
    return 'Good bye!'


OPERATORS = {
    'hello': handler_greetings,
    'close': handler_bye,
    'exit': handler_bye,
    'good bye': handler_bye,
    'add contact': handler_add,
    'add extra phone': handler_add_phone,
    'change phone': handler_update,
    'delete contact': handler_delete,
    'find contact by name': handler_find_by_name,
    'show all': handler_show_all,
    'find phone': handler_find_phone,
    'remove phone': handler_remove_phone
}


def main():
    print(f'use those commands:\n{BOT_COMMANDS}\n')
    while is_listening:
        user_line = input(f'listening...\n')
        if user_line is not None:
            try:
                command, data = parser(user_line)
                handler = get_handler(command)
                result = handler(data)
                print(result)
                continue
            except AttributeError:
                print(f'Please, type right command: {COMMANDS_RGX}')


if __name__ == '__main__':
    main()
