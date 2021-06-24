import config
import colorama
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL


def set_metadata(file):
    text = config.LOCALE
    track = EasyID3(file)
    metadata = dict()

    for data in text:
        if data in track.keys():
            print(colorama.Style.BRIGHT + text[data], end=' ')
            print(colorama.Style.DIM + '({1}): '.format(text[data], track[data][0]), end=' ')
            user_input = input()
            metadata[data] = user_input if user_input else track[data][0]

    return metadata


#
#
# def main():
#     print(set_metadata('./drafts/example2.mp3'))
#
#
# if __name__ == "__main__":
#     main()

print(set_metadata('P:\\id3-editor\\drafts\\example.mp3'))
