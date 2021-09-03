import os
from datetime import date
from mutagen.easyid3 import EasyID3


def get_norm_path(s: str) -> str:
    """
    Normalize the path, replace slashes if necessary

    :param s: the invalidated path
    :return: correct path
    """
    return os.path.normpath(s)


def get_new_filename(s: str) -> str:
    pass


def remove_brackets(s: str) -> str:
    """
    Remove text in the square brackets

    :param s: the string from which you need to remove the brackets
    :return: string without brackets
    """
    (split_symbol, index) = (']', 1) if s.startswith('[') else ('[', 0) if s.endswith(']') else ('\n', 0)
    return s.split(split_symbol)[index].strip(' ')


def validate_year(year: str) -> str:
    """
    Validate the value of year

    :param year: the value that needs to be validated
    :return: the value of the year param, if this value is a digit and is greater than 1800 and not greater than the
             current year, the empty string otherwise
    """
    if year.isdigit() and 1800 <= int(year) <= date.today().year:
        return year
    else:
        return ''


def validate_tracknumber(number: str) -> str:
    """
    Validate the value of tracknumber data

    :param number: the value that needs to be validated
    :return: the value of the number param before slash, if this value is a digit greater than 0 and not greater
             than 100
    """
    try:
        number = int(number.split('/')[0])
    except ValueError:
        return ''

    return number if 0 < number <= 100 else ''


def validate_data(track: EasyID3, data: str):
    """
    Call the necessary function for validating metadata depending on the parameter

    :param track: object with all metadata
    :param data: the current parameter
    :return: the right value for this parameter
    """
    try:
        value = track[data][0]
    except KeyError:
        return ''

    if data == 'date':
        return validate_year(value)
    elif data in {'title', 'artist', 'album', 'genre'}:
        return remove_brackets(value)
    elif data == 'tracknumber':
        return validate_tracknumber(value)


def replace_umlauts(s: str) -> str:
    """
    Replace special symbols with the letters with umlauts (ä, ö and ü)

    :param s: string with the special symbols (::)
    :return: edited string
    """
    return s.replace('a::', 'ä').replace('o::', 'ö').replace('u::', 'ü')


def validate_input(data: str):
    """
    Call the necessary function for validating data entered by the user

    :param data: the string that needs to be validated
    :return: edited string
    """
    return replace_umlauts(data)
