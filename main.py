import config
import colorama
import sys
import argparse
import json
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL
json_log = dict()


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
    return parser


def set_metadata(file, leave_copy=False, logging=False, *ignore):
    file = file.replace('\\', '/')
    text = config.LOCALE
    track = EasyID3(file)
    actual_data = set(track.keys())
    ignored_data = set(*ignore)
    file_title = file.split('/')[-1]
    print('\n' + colorama.Fore.GREEN + file_title + c_reset)

    # getting data from user and editing the metadata of the current file
    for data in text:
        if data in actual_data and data not in ignored_data:
            print(colorama.Style.BRIGHT + text[data] + c_reset + colorama.Style.DIM + ' ({0}): '.format(track[data][0]),
                  end=' ')
            user_input = input()
            track[data] = user_input if user_input else track[data][0]

    # deleting unnecessary data. wrong approach, will be fixed
    for data in actual_data:
        if (data == 'copyright' and not leave_copy) or \
                ((data not in text or data in ignored_data) and not (data == 'copyright' and leave_copy)):
            del track[data]

    if logging:
        json_log[file_title] = dict(track)
    track.save()
    return track


def main():
    ignored = set()
    leave_copy = False
    logging = False
    cli_parser = set_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])

    if namespace.minimal:
        ignored = ignored.union({'tracknumber', 'date'})
    if namespace.copyright:
        ignored.add('copyright')
        leave_copy = True
    if namespace.log:
        logging = True

    set_metadata('./drafts/example.mp3', leave_copy, logging, ignored)
    set_metadata('./drafts/example2.mp3', leave_copy, logging, ignored)

    if logging:
        with open('log.json', 'w', encoding='utf-8') as write_file:
            json.dump(json_log, write_file)


if __name__ == "__main__":
    set_parser()
    main()
