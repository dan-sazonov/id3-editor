import sys

import config

cli_parser = config.set_parser()
cli_args = cli_parser.parse_args(sys.argv[1:])

# namespace:
do_rename = cli_args.rename
leave_log = cli_args.log
leave_copy = cli_args.copyright

del_mode = cli_args.delete
parse_mode = cli_args.parse
scan_mode = cli_args.scan
min_mode = cli_args.minimal
rename_mode = cli_args.auto_rename

default = cli_args.title, cli_args.artist, cli_args.album, cli_args.number, cli_args.genre, cli_args.date
