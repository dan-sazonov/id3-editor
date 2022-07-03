import argparse

import colorama

VERSION = {
    'major': 1,
    'minor': 5,
    'micro': 0
}

AUTHOR = 'Dan Sazonov'

# if True, parser will be enabled
ENABLE_PARSER = True

# if True, dev mode will be enabled
DEV_MODE = True

# 'metadata key': 'text for CLI'
# don't change the keys! values could be translated to other languages
LOCALE = {
    'title': 'Title',
    'artist': 'Artist',
    'album': f'Album'
             f'{" <if you need to parse the value from Genius, enter [!]>" if ENABLE_PARSER else ""}',
    'tracknumber': 'Number of this track',
    'genre': 'Genre',
    'date': 'Year of release'
}

# path where the log will be saved
LOG_PATH = './logs/'

# data to be saved with the -c flag
COPYRIGHT = {'copyright', 'encodedby', 'organization', 'website'}

# if True, the data from the LEAVE_THIS_DATA will remain unchanged
LEAVE_SOME_DATA = False
LEAVE_THIS_DATA = ['tracknumber', 'date']  # don't change it!

# if True, the data entered by user won't be validated
SKIP_VALIDATION = False


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
    parser.add_argument('-s', '--scan', action='store_true', default=False,
                        help='create the log file with the current values of the metadata')
    parser.add_argument('-r', '--rename', action='store_true', default=False,
                        help='rename the files in the form of artist_track')
    parser.add_argument('--auto_rename', action='store_true', default=False,
                        help='rename the files in the form of artist_track without changing metadata')
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


class ColorMethods:
    def __init__(self):
        colorama.init()
        self.reset = colorama.Style.RESET_ALL
        self.red = colorama.Fore.RED
        self.green = colorama.Fore.GREEN
        self.bright = colorama.Style.BRIGHT
        self.dim = colorama.Style.DIM
