from datetime import date

from mutagen.easyid3 import EasyID3

import config


def remove_brackets(s: str) -> str:
    """
    Remove text in the square brackets

    :param s: the string from which you need to remove the brackets
    :return: string without brackets
    """
    (split_symbol, index) = (']', 1) if s.startswith('[') else ('[', 0) if s.endswith(']') else ('\n', 0)
    return s.split(split_symbol)[index].strip(' ')


def validate_for_url(data: tuple) -> list:
    """
    Remove all symbols and replace spaces with '-' in the strings of tuple

    :param data: tuple with str
    :return: list with formatted strings
    """
    arr = list(data)
    for s in range(len(arr)):
        arr[s] = arr[s].replace(' ', '-')
        arr[s] = ''.join(i if i.isalnum() or i == '-' else '' for i in arr[s])
    return arr


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

    return str(number) if 0 < number <= 100 else ''


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

    out = s.replace('A::', 'Ä').replace('O::', 'Ö').replace('U::', 'Ü').replace('a::', 'ä').replace('o::', 'ö') \
        .replace('u::', 'ü')
    return out


def validate_input(data: str, value: str):
    """
    Call the necessary function for validating data entered by the user

    :param data: the current parameter
    :param value: the string that needs to be validated
    :return: edited string
    """
    if config.SKIP_VALIDATION:
        return value

    value = value.strip('\xa0').strip('\t').strip('\n')

    if data in {'title', 'artist', 'album'}:
        return replace_umlauts(value)
    elif data == 'date':
        return validate_year(value)
    elif data == 'tracknumber':
        return validate_tracknumber(value)
    else:
        return value
