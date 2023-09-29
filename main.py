from user_actions_handler import get_handler
import globals
from utils.parser import parser, COMMANDS_RGX
from user_actions_handler import book
import pickle
from file_config import file

BOT_COMMANDS = 'hello\n' \
               'close\n' \
               'exit\n' \
               'good bye\n' \
               'add contact {name}(required) {phone}(required) {phone}(optional) X multiple bd:{birthday}(optional)\n' \
               'change phone {name}(r) {old phone}(r) {new phone}(r)\n' \
               'find contact by name {name}(r)\n' \
               'show all\n' \
               'add extra phone {name}(r) {new phone}(r)\n' \
               'find phone {name}(r) {phone}(r)\n' \
               'delete contact {name}(r)\n' \
               'remove phone {name}(r) {phone}(r)\n' \
               'find by key {key}(r)'


def main():
    print(f'use those commands:\n{BOT_COMMANDS}\n')
    while globals.is_listening:
        user_line = input(f'listening...\n')
        if user_line is not None:
            try:
                command, data = parser(user_line)
                handler = get_handler(command)
                result = handler(data)
                print(result)
                with open(file, "wb") as fh:
                    fh.write(pickle.dumps(book))

                continue
            except AttributeError:
                print(f'Please, type right command: {COMMANDS_RGX}')


if __name__ == '__main__':
    main()
