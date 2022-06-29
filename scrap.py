import requests
from bs4 import BeautifulSoup


def get_album_title(band, artist):
    url = f'https://genius.com/{band}-{artist}-lyrics'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.select('[href="#primary-album"]')[0].text


if __name__ == '__main__':
    tracks = ['mutter', 'sonne', 'puppe', 'radio', 'deutschland']

    for i in tracks:
        print(get_album_title('rammstein', i))
