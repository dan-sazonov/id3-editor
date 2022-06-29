import requests
from bs4 import BeautifulSoup
from validator import validate_for_url
from deep_translator import GoogleTranslator


def _translate(s):
    return GoogleTranslator(source='auto', target='en').translate(s)


def get_album_title(band, artist):
    band, artist = validate_for_url((_translate(band), _translate(artist)))
    url = f'https://genius.com/{band}-{artist}-lyrics'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    ans = soup.select('[href="#primary-album"]')
    return '' if not ans else ans[0].text.split(' (')[0]


if __name__ == '__main__':
    tracks = [('Blink-182', 'What’s My Age Again?'), ('saypink!', 'А Я ХОЧУ')]

    for i in tracks:
        print(get_album_title(*i))
