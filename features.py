import json

import mutagen
import pyperclip
from mutagen.easyid3 import EasyID3

import validator


def get_new_filename(track: EasyID3, number=0) -> str:
    """
    Get new filename for the track. Remove all symbols, replace spaces with underscores

    :param track: mutagen object, metadata of this track
    :param number: amount of the same files. if NOT 0 is got, this number will be added to the end of the filename
    :return: new filename looks like 'artist-file_name'
    """
    artist = '' if 'artist' not in track.keys() else track['artist'][0]
    title = '' if 'title' not in track.keys() else track['title'][0]

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


def write_json(file_name: str, content: dict) -> None:
    """
    Write 'file_name' to the file.json' content. If the file does not exist it will be created

    :param file_name: path to that file
    :param content: dict with the json-data
    :return: None
    """
    with open(file_name, 'w', encoding='utf-8') as write_file:
        json.dump(content, write_file, ensure_ascii=False)
