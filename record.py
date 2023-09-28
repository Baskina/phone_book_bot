import re
from error_handler import ShortNameError, WrongPhoneFormatError, PhoneNotExistError, WrongBirthdayFormatError
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__private_name = None
        self.name = value

    @property
    def name(self):
        return self.__private_name

    @name.setter
    def name(self, value):
        if not re.match(r'^(\D{3,})$', value):
            raise ShortNameError
        else:
            self.__private_name = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__private_phone = None
        self.phone = value

    @property
    def phone(self):
        return self.__private_phone

    @phone.setter
    def phone(self, value):
        if not re.match(r'^(\d{10})$', value):
            raise WrongPhoneFormatError
        else:
            self.__private_phone = value


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__private_birthday = None
        self.birthday = value

    @property
    def birthday(self):
        return self.__private_birthday

    @birthday.setter
    def birthday(self, value):
        if not re.match(r'(^0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4}$)', value):
            raise WrongBirthdayFormatError
        else:
            self.__private_birthday = datetime.strptime(value, '%d-%m-%Y')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = birthday
        self.phones = []

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now()
            delta1 = datetime(now.year, self.birthday.birthday.month, self.birthday.birthday.day)
            delta2 = datetime(now.year + 1, self.birthday.birthday.month, self.birthday.birthday.day)
            return ((delta1 if delta1 > now else delta2) - now).days
        else:
            return "There is no birthday data for this contact"

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
