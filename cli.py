import config
import sys

cli_parser = config.set_parser()
cli_args = cli_parser.parse_args(sys.argv[1:])

do_rename = cli_args.rename
