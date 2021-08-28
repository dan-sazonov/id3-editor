from datetime import date


def remove_brackets(s: str):
    """
    Remove text in the square brackets

    :param s: the string from which you need to remove the brackets
    :return: string without brackets
    """
    (split_symbol, index) = (']', 1) if s.startswith('[') else ('[', 0) if s.endswith(']') else ('\n', 0)
    return s.split(split_symbol)[index].strip(' ')


def validate_year(year):
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
