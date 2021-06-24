import config
import colorama
from mutagen.easyid3 import EasyID3

colorama.init()
c_reset = colorama.Style.RESET_ALL


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
    print(set_metadata('./drafts/example2.mp3'))


if __name__ == "__main__":
    main()

# print(set_metadata('P:\\id3-editor\\drafts\\example.mp3'))
