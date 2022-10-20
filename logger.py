import os
from datetime import datetime

import config
import features

np = os.path.normpath
c = config.ColorMethods()


def _get_log_file() -> str:
    """
    Searches for the last log file in the default directory

    :return: title of the file with path
    """
    log_path = np(config.LOG_PATH)
    files = []

    if os.path.exists(log_path):
        files = os.listdir(log_path)
        files = [file for file in files if file.split('.')[-1] == 'json']
        files = [np(os.path.join(log_path, file)) for file in files]
        files = [file for file in files if os.path.isfile(file)]

    return '' if not files else max(files, key=os.path.getctime)


def get_last_log() -> dict:
    """
    Returns the contents of the last log

    :return: dict from json
    """
    return features.read_json(_get_log_file())


def create_log() -> None:
    """
    Creates an empty log file and the necessary directory, if it is missing

    :return: None
    """
    file_name = datetime.today().isoformat('-').replace(':', '-').split('.')[0] + '.json'
    log_path = np(config.LOG_PATH)
    log_file_path = os.path.join(log_path, file_name)

    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    features.write_json(log_file_path)


def update_log(file: str, log: dict) -> None:
    """
    Add the 'log' dict for the 'file' track to the current log

    :param file: title of this track
    :param log: metadata
    :return: None
    """
    log_file = _get_log_file()
    cur_log = features.read_json(log_file)

    cur_log[file] = log
    features.write_json(log_file, cur_log)


def rename_logs_titles() -> None:
    """
    Rename the track names in the log according to the format

    :return: None
    """
    log_file = _get_log_file()
    cur_log = features.read_json(log_file)
    new_log = dict()

    for i in cur_log:
        title = features.get_new_filename(cur_log[i])

        number = 0
        while title in cur_log.keys():
            number += 1
            title = f'{title.split(" (")[0]} ({number})'

        new_log[title] = cur_log[i]

    features.write_json(log_file, new_log)


def rm_log() -> None:
    """
    Remove current log file

    :return: None
    """
    path = _get_log_file()
    if not path:
        return
    os.remove(path)


def parse_log():
    """
    Parse the json file with information about the file metadata

    :return: dict: 'filename' : {'metadata': 'value'}
    """
    rm_log()

    # find the later log file
    log_file = _get_log_file()
    log_file = np('<default file not found>' if not log_file else log_file)

    # ask the path to the log file
    print(f'{c.bright}Enter the absolute or relative path to the log file {c.reset}{c.dim} ({log_file}): ', end='')
    usr_input = input()
    log_file = np(usr_input) if usr_input else log_file

    if not os.path.exists(log_file):
        print(f'{c.red}err: {c.reset}The log file wasn\'t found. Make sure that the correct path is specified.')
        exit(1)

    features.read_json(log_file)
