import re

COMMANDS_RGX = 'hello|close|exit|good bye|' \
               'add contact|' \
               'change phone|' \
               'find contact by name|' \
               'show all|' \
               'add extra phone|' \
               'find phone|' \
               'delete contact|' \
               'remove phone|' \
               'find birthday|' \
               'find by key'


def parser(line):
    data_array = list(filter(None, re.split(COMMANDS_RGX, line)))
    command = re.search(COMMANDS_RGX, line)

    data = data_array[0].strip().split(' ') if len(data_array) > 0 else None
    return command.group(), data
