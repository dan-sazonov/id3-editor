import re

import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

from validator import validate_for_url


def _has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))


def _translate(s: str) -> str:
    """
    Translate from other languages to English

    :param s: string in any languages
    :return: string in English
    """

    return s if not _has_cyrillic(s) else GoogleTranslator(source='auto', target='en').translate(s)


def get_album_title(artist, track):
    """
    Parse genius.com and return album title. 'Artist' and 'track' will be validated and translated to English

    :param artist: name of the artist
    :param track: track title
    :return: title of the album
    """
    data = validate_for_url((_translate(artist), _translate(track)))
    url = f'https://genius.com/{data[0]}-{data[1]}-lyrics'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    ans = soup.select('[href="#primary-album"]')
    if not ans and response.status_code == 404:
        return ''
    if not ans and response.status_code == 200:
        return track
    return ans[0].text.split(' (')[0]
