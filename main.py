import config
import colorama
import sys
import os
import argparse
import json
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL
c_red = colorama.Fore.RED
c_green = colorama.Fore.GREEN
c_bright = colorama.Style.BRIGHT


def select_files():
    """
    Select files that need to be edited

    :returns: files - list of files that need to be edited; working_dir - directory where these files are placed
    """
    files = []
    print(c_bright + 'Enter the absolute or relative path to directory: ' + c_reset, end='')
    working_dir = input().replace('\\', '/')

    if not os.path.exists(working_dir):
        print(c_red + 'err: ' + c_reset + 'incorrect path. Try again.')
        exit(1)

    for file in os.listdir(working_dir):
        if file.split('.')[-1] == 'mp3':
            files.append(f'{working_dir}/{file}')
    return files, working_dir


def set_parser():
    """
    Set and configure the CLI argument parser

    :return: parser
    """
    parser = argparse.ArgumentParser(
        prog='id3-editor',
        description='''The simplest console tool for batch editing of mp3 metadata''',
        epilog='''(c) 2021, Dan Sazonov. Apache-2.0 License'''
    )

    parser.add_argument('-m', '--minimal', action='store_true', default=False,
                        help='set only title, artist, album and genre')
    parser.add_argument('-c', '--copyright', action='store_true', default=False,
                        help='leave the "copyright" parameter unchanged')
    parser.add_argument('-l', '--log', action='store_true', default=False,
                        help='create json log with all metadata')
    parser.add_argument('-p', '--parse', action='store_true', default=False,
                        help='parse json log and set this metadata')
    parser.add_argument('-d', '--delete', action='store_true', default=False,
                        help='delete all metadata from these tracks')
    parser.add_argument('-T', '--title', action='store_true', default=False,
                        help='set a title for all tracks')
    parser.add_argument('-R', '--artist', action='store_true', default=False,
                        help='set an artist for all tracks')
    parser.add_argument('-A', '--album', action='store_true', default=False,
                        help='set an album for all tracks')
    parser.add_argument('-N', '--number', action='store_true', default=False,
                        help='set a number for all tracks')
    parser.add_argument('-G', '--genre', action='store_true', default=False,
                        help='set a genre for all tracks')
    parser.add_argument('-D', '--date', action='store_true', default=False,
                        help='set a date for all tracks')
    return parser


def ask_user(file, default, ignore, leave_copy=False):
    """
    Ask the user for new metadata values

    :param file: the file to edit, str
    :param default: predefined metadata values, dict
    :param ignore: other metadata values to leave unchanged, dict
    :param leave_copy: True, if you need to leave copyright information, bool
    :return: dict with pairs 'metadata': 'value'
    """
    file = file.replace('\\', '/')
    file_title = file.split('/')[-1]
    text = config.LOCALE
    track = EasyID3(file)
    edited_md = dict()
    actual_data = set(track.keys())
    print('\n' + c_green + file_title + c_reset)

    # getting data from user and editing the metadata of the current file
    for data in text:
        if data in default:
            edited_md[data] = [default[data]]
        if data in ignore:
            # skip the iteration if the data in ignored or in default
            # (if the data in  ignored, then they are in default also)
            continue

        try:
            tmp = track[data][0]
        except KeyError:
            tmp = ''
        print(c_bright + text[data] + c_reset + colorama.Style.DIM + ' ({0}): '.format(tmp), end='')
        usr_input = input()
        edited_md[data] = [usr_input] if usr_input else [tmp]

    # leave information about the copyright holder
    if leave_copy:
        for data in config.COPYRIGHT:
            if data in actual_data:
                edited_md[data] = track[data][0]

    return edited_md


def set_defaults(title, artist, album, number, genre, date):
    """
    Ask the user for the values that need to be set for all files

    :param title: True, if you need to leave the title
    :param artist: True, if you need to leave the artist
    :param album: True, if you need to leave the album
    :param number: True, if you need to leave the number
    :param genre: True, if you need to leave the genre
    :param date: True, if you need to leave the date
    :return: default - dict with pairs 'metadata': 'predefined value'; ignored - set with data that should be ignored in
     ask_user
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
            print(c_bright + 'Set the {0} for all next tracks: '.format(data) + c_reset, end='')
            default[data] = input()
            ignored.add(data)

    return default, ignored


def parse_log():
    """
    Parse the json file with information about the file metadata

    :return: dict: 'filename' : {'metadata': 'value'}
    """
    try:
        with open(config.LOG_PATH, 'r') as read_file:
            return json.load(read_file)
    except FileNotFoundError:
        print(c_red + 'err: ' + c_reset + 'log.json doesn\'t exist. Try to run this program with [-l] flag.')
        exit(1)


def set_metadata(files, path, clear_all):
    """
    Set, edit or delete the metadata of the selected file

    :param files: dict, information about the metadata of each file
    :param path: str, the directory where these files are located
    :return: None
    """

    for file in files:
        current_path = os.path.join(path, file)
        # valid the path
        if not os.path.exists(current_path):
            print(c_red + 'warn: ' + c_reset + f'{current_path} doesn\'t exist. Try to run again.')
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

        track.save()


def main():
    """
    Main process

    :return: None
    """
    cli_parser = set_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])
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
            log[file_title] = dict() if namespace.delete else ask_user(file, default, ignored, namespace.copyright)

    # edit the metadata
    set_metadata(log, path, namespace.delete)

    if namespace.log and not namespace.parse:
        # create json file and put log into it
        with open(config.LOG_PATH, 'w', encoding='utf-8') as write_file:
            json.dump(log, write_file)

    print(c_green + '\nDone! Press [Enter] to exit')
    input()


if __name__ == "__main__":
    set_parser()
    main()
