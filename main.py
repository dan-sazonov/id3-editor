import config
import colorama
import sys
import argparse
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL

default_data = dict()


def set_parser():
    parser = argparse.ArgumentParser(
        prog='id3-editor',
        description='''The simplest console tool for batch editing of mp3 metadata''',
        epilog='''(c) 2021, Dan Sazonov. Apache-2.0 License'''
    )

    parser.add_argument('-m', '--minimal', action='store_true', default=False,
                        help='set only title, artist, album and genre')
    return parser


def set_metadata(file, *ignore):
    text = config.LOCALE
    track = EasyID3(file)
    actual_data = set(track.keys())
    ignored_data = set(*ignore)

    # getting data from user and editing the metadata of the current file
    for data in text:
        if data in actual_data and data not in ignored_data:
            print(colorama.Style.BRIGHT + text[data] + c_reset, end=' ')
            print(colorama.Style.DIM + '({0}): '.format(track[data][0]), end=' ')
            user_input = input()
            track[data] = user_input if user_input else track[data][0]

    # todo если надо что-то сохранить, здесь проверка на флаг

    # deleting unnecessary data. wrong approach, will be fixed
    for data in actual_data:
        if data not in text or data in ignored_data:
            del track[data]

    track.save()
    return track


def main():
    ignored = set()
    cli_parser = set_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])

    if namespace.minimal:
        # todo минимальный режим
        ignored = ignored.union({'tracknumber', 'date'})

    print(set_metadata('./drafts/example2.mp3', ignored))


if __name__ == "__main__":
    set_parser()
    main()
