import re
from user_actions_handler import handler_delete, handler_greetings, handler_update, handler_add, \
    handler_add_phone, handler_find_phone, handler_find_by_name, handler_remove_phone, handler_show_all, \
    handler_bye, handler_find_birthday
import globals

COMMANDS_RGX = 'hello|close|exit|good bye|' \
               'add contact|' \
               'change phone|' \
               'find contact by name|' \
               'show all|' \
               'add extra phone|' \
               'find phone|' \
               'delete contact|' \
               'remove phone|' \
               'find birthday'

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
               'remove phone {name}(r) {phone}(r)'


def parser(line):
    data_array = list(filter(None, re.split(COMMANDS_RGX, line)))
    command = re.search(COMMANDS_RGX, line)

    data = data_array[0].strip().split(' ') if len(data_array) > 0 else None
    return command.group(), data


def get_handler(operator):
    return OPERATORS[operator]


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
    'remove phone': handler_remove_phone,
    'find birthday': handler_find_birthday
}


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
                continue
            except AttributeError:
                print(f'Please, type right command: {COMMANDS_RGX}')


if __name__ == '__main__':
    main()
