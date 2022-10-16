import os
import sys

from mutagen.easyid3 import EasyID3

import cli
import config
import features
import logger
import validator
from scrap import get_album_title

np = os.path.normpath
c = config.ColorMethods()


def select_files():
    """
    Select files that need to be edited

    :return: list of files that need to be edited; working_dir - directory where these files are placed
    """
    files = []
    print(f'{c.bright}Enter the absolute or relative path to directory: {c.reset}', end='')
    working_dir = './drafts' if config.DEV_MODE else np(input())

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
    track = features.get_id3(file)

    edited_md = dict()
    actual_data = set(track.keys())

    features.copy_track_title(track)  # copy the title of this track to the clipboard
    print(f'\n{c.green}{file_title}{c.reset}')

    # getting data from user and editing the metadata of the current file
    i = 0
    while i < len(text):
        data = list(text.keys())[i]
        i += 1

        if data in default:
            edited_md[data] = [default[data]]
        if data in ignore:
            # skip the iteration if the data in ignored or in default
            # (if the data in  ignored, then they are in default also)
            continue

        # validate current value
        tmp = validator.validate_data(track, data)

        print(f'{c.bright}{text[data]}{c.reset}{c.dim} ({tmp}): ', end='')
        usr_input = input()
        if usr_input == '^':
            return dict(), True

        # parse the album title from genius.com
        if config.ENABLE_PARSER and data == 'album' and usr_input == '!':
            album = get_album_title(edited_md["artist"][0], edited_md["title"][0])
            if not album:
                print(f'{c.red}warn: {c.reset} incorrect data, or Genius doesn\'t have this track. ')
                i -= 1
                continue

            else:
                usr_input = album

        edited_md[data] = [validator.validate_input(data, usr_input)] if usr_input else [tmp]

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


def edit_files(path: str, clear_all: bool, do_rename: bool):
    """
    Set, edit or delete the metadata of the selected file and rename these files

    :param path: the directory where these files are located
    :param clear_all: True, if you need to remove all the metadata
    :param do_rename: True, if you need to rename files in the form of artist-track_title
    :return: None
    """
    renamed = dict()
    files = logger.get_last_log()
    for file in files:
        current_path = np(os.path.join(path, file))
        # valid the path
        if not os.path.exists(current_path):
            print(f'{c.red}warn: {c.reset}{current_path} doesn\'t exist. Try to run again.')
            continue

        track = features.get_id3(current_path)
        actual_data = set(files[file].keys())

        # set or edit metadata
        for data in files[file]:
            track[data] = files[file][data]

        # validate and leave unchanged some metadata
        if config.LEAVE_SOME_DATA:
            for i in config.LEAVE_THIS_DATA:
                if i in track.keys():
                    actual_data.add(i)
                    track[i] = [validator.validate_data(track, i)]

        # delete ignored metadata
        for del_data in track:
            if del_data not in actual_data or clear_all:
                del track[del_data]

        # save metadata and rename file
        track.save()
        if do_rename:
            file_name_tmp = features.get_new_filename(track)

            try:
                os.rename(current_path, np(f'{path}/{file_name_tmp}'))
            except FileExistsError:
                number = 0
                while os.path.exists(np(f'{path}/{file_name_tmp}')):
                    number += 1
                    file_name_tmp = features.get_new_filename(track, number)
                os.rename(current_path, np(f'{path}/{file_name_tmp}'))

            renamed[file] = file_name_tmp

    return renamed


def main():
    """
    Main process

    :return: None
    """
    # get the CLI arguments
    cli_args = cli.cli_args
    scan_mode = cli.scan_mode

    logger.create_log()

    # set the local variables
    mp3_files, path = select_files()
    default, ignored = set_defaults(cli_args.title, cli_args.artist, cli_args.album, cli_args.number,
                                    cli_args.genre, cli_args.date)

    if cli_args.minimal:
        ignored.update({'tracknumber', 'date'})
    if cli_args.copyright:
        ignored.update(config.COPYRIGHT)
    if not cli_args.parse:
        cur_index = 0
        while cur_index < len(mp3_files):
            file = mp3_files[cur_index]
            # ask for information about each file, fill in the log, or return to prev iteration
            file_title = os.path.split(file)[-1]
            tmp_log, need_returns = (dict(), False) if cli_args.delete else (dict(EasyID3(file)), False) \
                if (scan_mode or cli_args.auto_rename) else ask_user(file, default, ignored, cli_args.copyright)
            cur_index += -1 if need_returns else 1

            logger.update_log(file_title, tmp_log)

    # edit the files
    if not scan_mode:
        edit_files(path, cli_args.delete, (cli_args.rename or cli_args.auto_rename))

    if cli.do_rename:
        logger.rename_logs_titles()

    # create log file
    # if (cli_args.log or scan_mode) and not cli_args.parse:
    #     logger.create_logs(log, renamed_files)
    #     print(log, renamed_files)

    if not cli.leave_log:
        logger.rm_log()

    print(f'{c.green}\nDone! Press [Enter] to exit')
    input()


if __name__ == "__main__":
    main()
