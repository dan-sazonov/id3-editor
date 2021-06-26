import config
import colorama
import sys
import os
import argparse
import json
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL
usr_log = dict()


def select_files():
    files = []
    working_dir = input(colorama.Style.BRIGHT + 'Enter the absolute or relative path to directory: ' + c_reset).replace(
        '\\', '/')

    if not os.path.exists(working_dir):
        print(
            colorama.Fore.RED + 'err: ' + c_reset + 'incorrect path. Try again.')
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
    return parser


def ask_user(file, leave_copy=False, *ignore):
    file = file.replace('\\', '/')
    text = config.LOCALE
    track = EasyID3(file)
    edited_md = dict()
    actual_data = set(track.keys())
    ignored_data = set(*ignore)
    file_title = file.split('/')[-1]
    print('\n' + colorama.Fore.GREEN + file_title + c_reset)

    # getting data from user and editing the metadata of the current file
    for data in text:
        if data in actual_data and data not in ignored_data:
            print(colorama.Style.BRIGHT + text[data] + c_reset + colorama.Style.DIM + ' ({0}): '.format(track[data][0]),
                  end=' ')
            usr_input = input()
            edited_md[data] = [usr_input] if usr_input else [track[data][0]]

    if leave_copy and 'copyright' in actual_data:
        edited_md['copyright'] = [track['copyright'][0]]

    return edited_md


def parse_log():
    try:
        with open('log.json', 'r') as read_file:
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

        for data in track:
            if data in actual_data:
                track[data] = files[file][data]
            else:
                track[data] = u''
        track.save()


def main():
    ignored = set()
    leave_copy = False
    logging = False
    log = usr_log
    mp3_files, path = select_files()
    cli_parser = set_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])

    if namespace.minimal:
        ignored = ignored.union({'tracknumber', 'date'})
    if namespace.copyright:
        ignored.add('copyright')
        leave_copy = True
    if namespace.log:
        logging = True
    if namespace.parse:
        log = parse_log()
    else:
        for file in mp3_files:
            file_title = file.split('/')[-1]
            log[file_title] = ask_user(file, leave_copy, ignored)

    set_metadata(log, path)

    if logging:
        with open('log.json', 'w', encoding='utf-8') as write_file:
            json.dump(log, write_file)


if __name__ == "__main__":
    set_parser()
    main()
    parse_log()
