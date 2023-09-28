class WrongPhoneFormatError(ValueError):
    pass


class WrongBirthdayFormatError(Exception):
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
        except WrongBirthdayFormatError:
            return 'Wrong birthday format, please type dd-mm-yyyy'
        except Exception as error:
            return f'Something happens: {error}'

    return error_handler
