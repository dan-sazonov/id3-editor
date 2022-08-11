import mutagen
import pyperclip
from mutagen.easyid3 import EasyID3

import validator


def get_new_filename(artist: str, title: str, number=0) -> str:
    """
    Get new filename for the track. Remove all symbols, replace spaces with underscores

    :param number: amount of the same files. if NOT 0 is got, this number will be added to the end of the filename
    :param artist: artist of this track
    :param title: title of this track
    :return: new filename looks like 'artist-file_name'
    """

    tmp_data = []
    for data in [artist, title]:
        tmp_data.append(''.join([i.lower() if i != ' ' else '_' for i in data if i.isalnum() or i == ' ']))

    return '{0}-{1} ({2}).mp3'.format(*tmp_data, number) if number else '{0}-{1}.mp3'.format(*tmp_data)


def get_track_title(track: EasyID3) -> list[str, str]:
    """
    Get artist and title from the track

    :param track: mutagen object, metadata of this track
    :return: list[artist, title]. Artist and title will be the empty strings if the track hasn't such tags
    """
    clip = []
    for data in 'artist', 'title':
        if data in track.keys():
            clip.append(validator.remove_brackets(track[data][0]))
        else:
            clip.append('')
    return clip


def copy_track_title(track: EasyID3) -> None:
    """
    Save artist and title of this track to the clipboard

    :param track: mutagen object, metadata of this track
    :return: None
    """
    artist, title = get_track_title(track)
    clip = f'{artist} - {title}'
    pyperclip.copy(clip)


def get_id3(file: str) -> EasyID3:
    """
    Add id3 attributes to the empty mp3 file

    :param file: path to the mp3 file
    :return: the same file with empty metadata attributes
    """
    try:
        track = EasyID3(file)
    except mutagen.MutagenError:
        track = mutagen.File(file, easy=True)
        track.add_tags()

    return track
