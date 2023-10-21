import os

import colorama

VERSION = {
    'major': 1,
    'minor': 6,
    'micro': 1
}

AUTHOR = 'Dan Sazonov'

# if True, parser will be enabled
ENABLE_PARSER = True

# if True, dev mode will be enabled
# abandon hope, everyone who enters here
DEV_MODE = os.getenv('DEV_MODE') == '1' or os.getenv('DEV_MODE'.lower()) == 'true'

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
LEAVE_SOME_DATA = True
LEAVE_THIS_DATA = ['tracknumber', 'date']

# if True, the data entered by user won't be validated
SKIP_VALIDATION = False

# in 'min-scan' mode, data from the output is copied to the clipboard if True
DO_OUTPUT_COPY = True


class ColorMethods:
    def __init__(self):
        colorama.init()
        self.reset = colorama.Style.RESET_ALL
        self.red = colorama.Fore.RED
        self.green = colorama.Fore.GREEN
        self.bright = colorama.Style.BRIGHT
        self.dim = colorama.Style.DIM
