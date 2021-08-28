def remove_brackets(s: str):
    """
    Remove text in the square brackets

    :param s: the string from which you need to remove the brackets
    :return: string without brackets
    """
    (split_symbol, index) = (']', 1) if s.startswith('[') else ('[', 0) if s.endswith(']') else ('\n', 0)
    return s.split(split_symbol)[index].strip(' ')
