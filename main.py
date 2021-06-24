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
        description='''The simplest console tool for batch editing of mp3 metadata.''',
        epilog='''(c) 2021, Dan Sazonov. Apache-2.0 License'''
    )
    return parser


def set_metadata(file):
    text = config.LOCALE
    track = EasyID3(file)

    # getting data from user and editing the metadata of the current file
    for data in text:
        if data in track.keys():
            print(colorama.Style.BRIGHT + text[data] + c_reset, end=' ')
            print(colorama.Style.DIM + '({0}): '.format(track[data][0]), end=' ')
            user_input = input()
            track[data] = user_input if user_input else track[data][0]

    # todo если надо что-то сохранить, здесь проверка на флаг

    # deleting unnecessary data. wrong approach, will be fixed
    for data in track:
        if data not in text:
            del track[data]

    track.save()
    return track


def main():
    cli_parser = set_parser()
    namespace = cli_parser.parse_args(sys.argv[1:])

    print(namespace)
    print(set_metadata('./drafts/example2.mp3'))


if __name__ == "__main__":
    set_parser()
    main()

# print(set_metadata('P:\\id3-editor\\drafts\\example.mp3'))
