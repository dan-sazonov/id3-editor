import config
import colorama
import sys
import os
import argparse
import json
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL


def select_files():
    files = []
    print(colorama.Style.BRIGHT + 'Enter the absolute or relative path to directory: ' + c_reset, end='')
    working_dir = input().replace('\\', '/')

    if not os.path.exists(working_dir):
        print(colorama.Fore.RED + 'err: ' + c_reset + 'incorrect path. Try again.')
        exit(1)

    for file in os.listdir(working_dir):
        if file.split('.')[-1] == 'mp3':
            files.append(f'{working_dir}/{file}')
    return files, working_dir


def set_parser():
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
    file = file.replace('\\', '/')
    file_title = file.split('/')[-1]
    text = config.LOCALE
    track = EasyID3(file)
    edited_md = dict()
    actual_data = set(track.keys())
    ignored_data = set(ignore)
    print('\n' + colorama.Fore.GREEN + file_title + c_reset)

    # getting data from user and editing the metadata of the current file
    for data in text:
        if data in default:
            edited_md[data] = [default[data]]

        if data in ignored_data:
            continue
        try:
            tmp = track[data][0]
        except KeyError:
            tmp = ''
        print(colorama.Style.BRIGHT + text[data] + c_reset + colorama.Style.DIM + ' ({0}): '.format(tmp),
              end=' ')
        usr_input = input()
        edited_md[data] = [usr_input] if usr_input else [tmp]

    # leave information about the copyright holder
    if leave_copy:
        for data in config.COPYRIGHT:
            if data in actual_data:
                edited_md[data] = track[data][0]

    return edited_md


def set_defaults(title, artist, album, number, genre, date):
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
            print(colorama.Style.BRIGHT + 'Set the {0} for all next tracks: '.format(data) + c_reset, end='')
            default[data] = input()
            ignored.add(data)

    return default, ignored


def parse_log():
    try:
        with open(config.LOG_PATH, 'r') as read_file:
            return json.load(read_file)
    except FileNotFoundError:
        print(
            colorama.Fore.RED + 'err: ' + c_reset + 'log.json doesn\'t exist. Try to run this program with [-l] flag.')
        exit(1)


def set_metadata(files, path):
    for file in files:
        current_path = os.path.join(path, file)
        track = EasyID3(current_path)
        actual_data = files[file].keys()

        for data in files[file]:
            track[data] = files[file][data]
        for del_data in track:
            if del_data not in actual_data:
                del track[del_data]

        track.save()


def main():
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
            file_title = file.split('/')[-1]
            log[file_title] = ask_user(file, default, ignored, namespace.copyright)

    set_metadata(log, path)

    if namespace.log:
        with open(config.LOG_PATH, 'w', encoding='utf-8') as write_file:
            json.dump(log, write_file)

    print(colorama.Fore.GREEN + '\nDone! Press [Enter] to exit')
    input()


if __name__ == "__main__":
    set_parser()
    main()
