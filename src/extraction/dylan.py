import json

from bs4 import BeautifulSoup
from extraction.util import cached_get

def parse_index(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    (lst,) = soup.find_all(id='item-list')
    for el in lst.find_all('div', class_='line line_detail'):
        song_el = el.find('span', class_='song')
        album_el = el.find('span', class_='release')

        title = song_el.text
        link = song_el.a.attrs['href']
        album = album_el.text
        yield (title, album, link)


def parse_song(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    root = soup.article

    title = root.find('h2').text.strip()
    credit_el = root.find('div', class_='credit')
    credit = credit_el.text.strip() if credit_el else ''
    lyrics = root.find('div', class_='lyrics')
    copy = root.find('p', class_='copytext')
    copytext = copy.get_text(strip=True) if copy else ''
    text = lyrics.get_text().replace(copytext, '')

    return (title, credit, text)


def all_tracks():
    html = cached_get('https://www.bobdylan.com/songs/?may=filters&order=desc')
    for (title, album, href) in parse_index(html):
        html = cached_get(href)

        (title2, credit, text) = parse_song(html)
        assert title == title2

        yield {
            'title': title,
            'album': album,
            'lyrics': text,
            'credit': credit,
        }

def main():
    with open('dylan.txt', 'w') as fp:
        html = cached_get('https://www.bobdylan.com/songs/?may=filters&order=desc')
        for (title, album, href) in parse_index(html):
            print(title)
            html = cached_get(href)

            (title2, credit, text) = parse_song(html)
            assert title == title2

            row = (title, album, credit, text)
            fp.write(json.dumps(row)+'\n')
