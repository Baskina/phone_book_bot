from collections import UserDict


class RecordsPerPageIterator:
    def __init__(self, book, n=2):
        self.step = n
        self.max_index = len(book)
        self.first_index_on_page = 0
        self.records = []
        self.data = book

    def __next__(self):
        if self.first_index_on_page < self.max_index:
            self.records = list(self.data.values())[self.first_index_on_page: self.first_index_on_page + self.step]
            self.first_index_on_page += self.step
            return self.records
        raise StopIteration


class AddressBook(UserDict):

    def __iter__(self):
        return RecordsPerPageIterator(self.data)

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
