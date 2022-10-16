import json
import os
from datetime import datetime

import config

np = os.path.normpath
c = config.ColorMethods()


def create_logs(log: dict, renamed: dict):
    """
    Create json file and save the log in it

    :param log: the data to be saved
    :param renamed: dict like this: {'old_file_name.mp3': 'new_file_name.mp3'}
    :return: None
    """
    file_name = datetime.today().isoformat('-').replace(':', '-').split('.')[0] + '.json'
    log_path = np(config.LOG_PATH)
    log_file_path = os.path.join(log_path, file_name)
    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    if renamed:
        # rename the files in the log
        log_tmp = {renamed[i]: log[i] for i in log}
        log = log_tmp
        del log_tmp

    with open(log_file_path, 'w', encoding='utf-8') as write_file:
        json.dump(log, write_file, ensure_ascii=False)


def parse_log():
    """
    Parse the json file with information about the file metadata

    :return: dict: 'filename' : {'metadata': 'value'}
    """

    # find the later log file
    log_path = np(config.LOG_PATH)
    files = os.listdir(log_path)
    files = [file for file in files if file.split('.')[-1] == 'json']
    files = [np(os.path.join(log_path, file)) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    log_file = np('<default file not found>' if not files else max(files, key=os.path.getctime))

    # ask the path to the log file
    print(f'{c.bright}Enter the absolute or relative path to the log file {c.reset}{c.dim} ({log_file}): ', end='')
    usr_input = input()
    log_file = np(usr_input) if usr_input else log_file

    if not os.path.exists(log_file):
        print(f'{c.red}err: {c.reset}The log file wasn\'t found. Make sure that the correct path is specified.')
        exit(1)

    # read log
    with open(log_file, 'r', encoding='utf-8') as read_file:
        return json.load(read_file)
