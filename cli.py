import argparse
import sys


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
    parser.add_argument('--min_scan', action='store_true', default=False,
                        help='print out "artist-title" pairs for all tracks')
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


cli_parser = set_parser()
cli_args = cli_parser.parse_args(sys.argv[1:])

# namespace:
do_rename = cli_args.rename
leave_log = cli_args.log
leave_copy = cli_args.copyright

del_mode = cli_args.delete
parse_mode = cli_args.parse
scan_mode = cli_args.scan
min_scan = cli_args.min_scan
min_mode = cli_args.minimal
rename_mode = cli_args.auto_rename

default = cli_args.title, cli_args.artist, cli_args.album, cli_args.number, cli_args.genre, cli_args.date
