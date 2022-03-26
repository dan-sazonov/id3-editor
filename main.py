import json
import os
import sys

from mutagen.easyid3 import EasyID3

import config
import features
import logger

np = os.path.normpath
c = config.ColorMethods()


def select_files():
    """
    Select files that need to be edited

    :return: list of files that need to be edited; working_dir - directory where these files are placed
    """
    files = []
    print(f'{c.bright}Enter the absolute or relative path to directory: {c.reset}', end='')
    working_dir = np(input())

    if not os.path.exists(working_dir):
        print(f'{c.red}err: {c.reset}incorrect path. Try again.')
        exit(1)

    for file in os.listdir(working_dir):
        if file.split('.')[-1] == 'mp3':
            files.append(np(f'{working_dir}/{file}'))
    return files, working_dir


def ask_user(file: str, default: dict, ignore: set, leave_copy: bool = False):
    """
    Ask the user for new metadata values

    :param file: the file to edit
    :param default: predefined metadata values
    :param ignore: other metadata values to leave unchanged
    :param leave_copy: bool, True, if you need to leave copyright information
    :return: dict with pairs 'metadata': 'value'; bool var: True, if you need to return to the prev iteration
    """
    file = np(file)
    file_title = os.path.split(file)[-1]
    text = config.LOCALE
    track = EasyID3(file)
    edited_md = dict()
    actual_data = set(track.keys())
    print(f'\n{c.green}{file_title}{c.reset}')

    # getting data from user and editing the metadata of the current file
    for data in text:
        if data in default:
            edited_md[data] = [default[data]]
        if data in ignore:
            # skip the iteration if the data in ignored or in default
            # (if the data in  ignored, then they are in default also)
            continue

        # validate current value
        tmp = features.validate_data(track, data)

        print(f'{c.bright}{text[data]}{c.reset}{c.dim} ({tmp}): ', end='')
        usr_input = input()
        if usr_input == '^':
            return dict(), True
        edited_md[data] = [features.validate_input(data, usr_input)] if usr_input else [tmp]

    # leave information about the copyright holder
    if leave_copy:
        for data in config.COPYRIGHT:
            if data in actual_data:
                edited_md[data] = track[data][0]

    return edited_md, False


def set_defaults(title: bool, artist: bool, album: bool, number: bool, genre: bool, date: bool):
    """
    Ask the user for the values that need to be set for all files

    :param title: True, if you need to leave the title
    :param artist: True, if you need to leave the artist
    :param album: True, if you need to leave the album
    :param number: True, if you need to leave the number
    :param genre: True, if you need to leave the genre
    :param date: True, if you need to leave the date
    :return: default: dict with pairs 'metadata': 'predefined value';
             ignored: set with data that should be ignored in ask_user
    """
    default = dict()
    ignored = set()
    args = {'title': title,
            'artist': artist,
            'album': album,
            'tracknumber': number,
            'genre': genre,
            'date': date}

    for data in args:
        if args[data]:
            print(f'{c.bright}Set the {data} for all next tracks: {c.reset}', end='')
            default[data] = input()
            ignored.add(data)

    return default, ignored


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
    print(f'{c.bright}Enter the absolute or relative path to the log file: {c.reset}{c.dim} ({log_file}): ', end='')
    usr_input = input()
    log_file = np(usr_input) if usr_input else log_file

    if not os.path.exists(log_file):
        print(f'{c.red}err: {c.reset}The log file wasn\'t found. Make sure that the correct path is specified.')
        exit(1)

    # read log
    with open(log_file, 'r', encoding='utf-8') as read_file:
        return json.load(read_file)


def edit_files(files: dict, path: str, clear_all: bool, do_rename: bool):
    """
    Set, edit or delete the metadata of the selected file and rename these files

    :param files: information from user about the metadata of each file
    :param path: the directory where these files are located
    :param clear_all: True, if you need to remove all the metadata
    :param do_rename: True, if you need to rename files in the form of artist-track_title
    :return: None
    """
    renamed = dict()
    for file in files:
        current_path = np(os.path.join(path, file))
        # valid the path
        if not os.path.exists(current_path):
            print(f'{c.red}warn: {c.reset}{current_path} doesn\'t exist. Try to run again.')
            continue
        track = EasyID3(current_path)
        actual_data = set(files[file].keys())

        # set or edit metadata
        for data in files[file]:
            track[data] = files[file][data]

        # validate and leave unchanged some metadata
        if config.LEAVE_SOME_DATA:
            for i in config.LEAVE_THIS_DATA:
                if i in track.keys():
                    actual_data.add(i)
                    track[i] = [features.validate_data(track, i)]

        # delete ignored metadata
        for del_data in track:
            if del_data not in actual_data or clear_all:
                del track[del_data]

        # save metadata and rename file
        track.save()
        if do_rename:
            file_name_tmp = features.get_new_filename(track['artist'][0], track['title'][0])
            os.rename(current_path, np(f'{path}/{file_name_tmp}'))
            renamed[file] = file_name_tmp

    return renamed


def main():
    """
    Main process

    :return: None
    """
    # get the CLI arguments
    cli_parser = config.set_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])
    scan_mode = namespace.scan
    log = parse_log() if namespace.parse else dict()

    # set the local variables
    renamed_files = False
    mp3_files, path = select_files()
    default, ignored = set_defaults(namespace.title, namespace.artist, namespace.album, namespace.number,
                                    namespace.genre, namespace.date)

    if namespace.minimal:
        ignored.update({'tracknumber', 'date'})
    if namespace.copyright:
        ignored.update(config.COPYRIGHT)
    if not namespace.parse:
        cur_index = 0
        while cur_index < len(mp3_files):
            file = mp3_files[cur_index]
            # ask for information about each file, fill in the log, or return to prev iteration
            file_title = os.path.split(file)[-1]
            log[file_title], need_returns = (dict(), False) if namespace.delete else (dict(EasyID3(file)), False) \
                if (scan_mode or namespace.auto_rename) else ask_user(file, default, ignored, namespace.copyright)
            cur_index += -1 if need_returns else 1

    # edit the files
    if not scan_mode:
        renamed_files = edit_files(log, path, namespace.delete, (namespace.rename or namespace.auto_rename))

    # create log file
    if (namespace.log or scan_mode) and not namespace.parse:
        logger.create_logs(log, renamed_files)

    print(f'{c.green}\nDone! Press [Enter] to exit')
    input()


if __name__ == "__main__":
    main()
