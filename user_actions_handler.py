from error_handler import input_error
from record import Record
from error_handler import EmptyNameError, EmptyPhoneNumberError
from contact_book import AddressBook
import globals

book = AddressBook()


@input_error
def handler_add(data):
    if not data or len(data) < 1 or not data[0]:
        raise EmptyNameError

    bd = None
    for item in data[1:]:
        if item.startswith('bd:'):
            bd = item.split('bd:')[1]
    record = Record(data[0], bd)

    if len(data) < 2:
        raise EmptyPhoneNumberError

    for phone in data[1:]:
        if not phone.startswith('bd:'):
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


@input_error
def handler_show_all(*args):
    if not book:
        return 'No names in your phone book'
    contact_list = ''
    for index, book_contact_list in enumerate(book):
        print(f'Contacts per {index + 1} page')
        for contact in book_contact_list:
            print(contact)

    print('In one list:')
    for name, value in book.data.items():
        phones = '; '.join(list(map(lambda x: x.value, value.phones)))
        birthday = value.birthday.value if value.birthday else ''
        days_before_birthday = value.days_to_birthday() if value.birthday else ''
        contact_list += 'Name: {} --- Phones: {} --- Birthday: {} ---- Days before birthday: {}\n' \
            .format(name, phones, birthday, days_before_birthday)
    return contact_list


@input_error
def handler_find_birthday(data):
    record = book.find(data[0])
    return 'Birthday: {} ---- Days before birthday: {}\n'.format(record.birthday.value, record.days_to_birthday()) \
        if record.birthday else 'There no birthday field'


@input_error
def handler_delete(data):
    return book.delete(data[0])


def handler_greetings(*args):
    return 'How can I help you?'


def handler_bye(*args):
    globals.is_listening = False
    return 'Good bye!'
