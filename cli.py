import config
import sys

cli_parser = config.set_parser()
cli_args = cli_parser.parse_args(sys.argv[1:])


# namespace:
do_rename = cli_args.rename
parse_mode = cli_args.parse
leave_log = cli_args.log
scan_mode = cli_args.scan
