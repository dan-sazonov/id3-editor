import config
import features
import colorama
import sys
import os
import json
from datetime import datetime
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL
c_red = colorama.Fore.RED
c_green = colorama.Fore.GREEN
c_bright = colorama.Style.BRIGHT
c_dim = colorama.Style.DIM


def select_files():
    """
    Select files that need to be edited

    :return: list of files that need to be edited; working_dir - directory where these files are placed
    """
    files = []
    print(f'{c_bright}Enter the absolute or relative path to directory: {c_reset}', end='')
    working_dir = input().replace('\\', '/')

    if not os.path.exists(working_dir):
        print(f'{c_red}err: {c_reset}incorrect path. Try again.')
        exit(1)

    for file in os.listdir(working_dir):
        if file.split('.')[-1] == 'mp3':
            files.append(f'{working_dir}/{file}')
    return files, working_dir


def ask_user(file: str, default: dict, ignore: set, leave_copy: bool = False):
    """
    Ask the user for new metadata values

    :param file: the file to edit
    :param default: predefined metadata values
    :param ignore: other metadata values to leave unchanged
    :param leave_copy: bool, True, if you need to leave copyright information
    :return: dict with pairs 'metadata': 'value'
    """
    file = file.replace('\\', '/')
    file_title = file.split('/')[-1]
    text = config.LOCALE
    track = EasyID3(file)
    edited_md = dict()
    actual_data = set(track.keys())
    print(f'\n{c_green}{file_title}{c_reset}')

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

        print(f'{c_bright}{text[data]}{c_reset}{c_dim} ({tmp}): ', end='')
        usr_input = input()
        edited_md[data] = [usr_input] if usr_input else [tmp]

    # leave information about the copyright holder
    if leave_copy:
        for data in config.COPYRIGHT:
            if data in actual_data:
                edited_md[data] = track[data][0]

    return edited_md


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
            print(f'{c_bright}Set the {data} for all next tracks: {c_reset}', end='')
            default[data] = input()
            ignored.add(data)

    return default, ignored


def parse_log():
    """
    Parse the json file with information about the file metadata

    :return: dict: 'filename' : {'metadata': 'value'}
    """

    # find the later log file
    files = os.listdir(config.LOG_PATH)
    files = [file for file in files if file.split('.')[-1] == 'json']
    files = [os.path.join(config.LOG_PATH, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    log_file = '<default file not found>' if not files else max(files, key=os.path.getctime)

    # ask the path to the log file
    print(f'{c_bright}Enter the absolute or relative path to the log file: {c_reset}{c_dim} ({log_file}): ', end='')
    usr_input = input()
    log_file = usr_input if usr_input else log_file

    if not os.path.exists(log_file):
        print(f'{c_red}err: {c_reset}The log file wasn\'t found. Make sure that the correct path is specified.')
        exit(1)

    # read log
    with open(log_file, 'r') as read_file:
        return json.load(read_file)


def set_metadata(files: dict, path: str, clear_all: bool, do_rename: bool):
    """
    Set, edit or delete the metadata of the selected file

    :param files: information about the metadata of each file
    :param path: the directory where these files are located
    :param clear_all: True, if you need to remove all the metadata
    :param do_rename: True, if you need to rename files in the form of artist-track_title
    :return: None
    """

    for file in files:
        current_path = os.path.join(path, file)
        # valid the path
        if not os.path.exists(current_path):
            print(f'{c_red}warn: {c_reset}{current_path} doesn\'t exist. Try to run again.')
            continue
        track = EasyID3(current_path)
        actual_data = files[file].keys()

        # set or edit metadata
        for data in files[file]:
            track[data] = files[file][data]

        # delete ignored metadata
        for del_data in track:
            if del_data not in actual_data or clear_all:
                del track[del_data]

        # save metadata and rename file
        track.save()
        if do_rename:
            os.rename(current_path, f'{track["artist"][0].replace(" ", "_")}-{track["title"][0].replace(" ", "_")}.mp3')


def create_logs(log: dict):
    """
    Create json file and save the log in it

    :param log: the data to be saved
    :return: None
    """
    file_name = datetime.today().isoformat('-').replace(':', '-').split('.')[0] + '.json'
    log_path = os.path.join(config.LOG_PATH, file_name)
    if not os.path.isdir(config.LOG_PATH):
        os.mkdir(config.LOG_PATH)

    with open(log_path, 'w', encoding='utf-8') as write_file:
        json.dump(log, write_file)


def main():
    """
    Main process

    :return: None
    """
    cli_parser = config.set_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])
    scan_mode = namespace.scan
    log = parse_log() if namespace.parse else dict()
    mp3_files, path = select_files()
    default, ignored = set_defaults(namespace.title, namespace.artist, namespace.album, namespace.number,
                                    namespace.genre, namespace.date)

    if namespace.minimal:
        ignored.update({'tracknumber', 'date'})
    if namespace.copyright:
        ignored.update(config.COPYRIGHT)
    if not namespace.parse:
        for file in mp3_files:
            # ask for information about each file, fill in the log
            file_title = file.split('/')[-1]
            log[file_title] = dict() if namespace.delete else dict(EasyID3(file)) if scan_mode \
                else ask_user(file, default, ignored, namespace.copyright)

    # edit the metadata
    if not scan_mode:
        set_metadata(log, path, namespace.delete, namespace.rename)

    if (namespace.log or scan_mode) and not namespace.parse:
        create_logs(log)

    print(f'{c_green}\nDone! Press [Enter] to exit')
    input()


if __name__ == "__main__":
    main()
