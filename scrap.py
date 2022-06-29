import requests
from bs4 import BeautifulSoup
from validator import validate_for_url


def get_album_title(band, artist):
    band, artist = validate_for_url((band, artist))
    url = f'https://genius.com/{band}-{artist}-lyrics'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    ans = soup.select('[href="#primary-album"]')
    return '' if not ans else ans[0].text

# todo стрипать все что в скобках
# todo переводить с русского название трека и группу


if __name__ == '__main__':
    tracks = [('Blink-182', 'What’s My Age Again?'), ('saypink!', 'AND I WANT')]

    for i in tracks:
        print(get_album_title(*i))
