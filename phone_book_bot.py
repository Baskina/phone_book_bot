import re

is_listening = True
phone_book = {}
COMMANDS_RGX = 'hello|close|exit|good bye|add|change|phone|show all'


def input_error(handler):
    def error_handler(data):
        try:
            handler(data)
        except TypeError as error:
            print(f'{error}: Give me name and/or phone please')
        except IndexError as error:
            print(f'{error}: Give me name and/or phone please')

    return error_handler


def handler_show_all(*args):
    if not phone_book:
        print('No names in your phone book')
        return
    for name, phone in phone_book.items():
        print("Name: {} --- Phone: {}".format(name, phone))


@input_error
def handler_find_name(data):
    if data[0]:
        for name in list(filter(lambda x: phone_book[x] == data[0], phone_book)):
            print(name)


@input_error
def handler_add(data):
    if data[0] in phone_book.keys():
        data[0] = data[0] + "\U0001f600"
    phone_book.update({data[0]: data[1]})


@input_error
def handler_update(data):
    phone_book.update({data[0]: data[1]})


def handler_greetings(*args):
    print("How can I help you?")


def handler_bye(*args):
    print("Good bye!")
    global is_listening
    is_listening = False


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
    'add': handler_add,
    'change': handler_update,
    'phone': handler_find_name,
    'show all': handler_show_all
}


def main():
    while is_listening:
        user_line = input('listening...\n')
        if user_line is not None:
            try:
                command, data = parser(user_line)
                handler = get_handler(command)
                handler(data)
                continue
            except AttributeError:
                print(f'Please, type right command: {COMMANDS_RGX}')


if __name__ == '__main__':
    main()
