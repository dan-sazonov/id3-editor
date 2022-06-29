import requests
from bs4 import BeautifulSoup

tracks = ['mutter', 'sonne', 'puppe', 'radio', 'deutschland']


def get_album_title(band, track):
    url = f'https://genius.com/{band}-{track}-lyrics'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.select('[href="#primary-album"]')[0].text


for i in tracks:
    print(get_album_title('rammstein', i))
