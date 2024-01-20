import argparse
import itertools
import json

from bs4 import BeautifulSoup

from extraction.util import cached_get

TS = 1177

def song_meta(song_id):
    url = f'https://genius.com/api/songs/{song_id}'
    resp = cached_get(url)
    data = json.loads(resp)['response']['song']

    albums = [
        {'id': a['id'], 'title': a['name'], 'artist': a['artist']['name']}
        for a in data['albums']
        if a['artist']['id'] == data['primary_artist']['id']
    ]
    albums = sorted(albums, key=lambda x: x['id'])

    rels = [
        x['songs'] for x in data['song_relationships']
        if x['relationship_type'] in ['remix_of', 'cover_of', 'live_version_of']
    ]

    return {
        'url': data['url'],
        'is_music': data['is_music'],
        'albums': albums,
        'related': [x['title'] for x in itertools.chain(*rels)],
    }


def songs_for_artist(artist_id):
    def fetch_artist_songs(artist_id):
        page = 1
        while True:
            url = f'https://genius.com/api/artists/{artist_id}/songs?page={page}&sort=title'
            resp = cached_get(url)
            data = json.loads(resp)

            if not data['response']['next_page']:
                break
            for song in data['response']['songs']:
                yield song
            page += 1

    for song in fetch_artist_songs(artist_id):
        if song['primary_artist']['id'] != artist_id:
            continue
        meta = song_meta(song['id'])

        if not meta['is_music']:
            continue
        if meta['related']:
            continue
        if not meta['albums']:
            continue
        # todo: can filter by meta['albums']

        yield {
            'title': song['title'],
            'album': meta['albums'][0]['title'],
            'lyrics': song_lyrics(song['url'])
        }

def parse_lyrics(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    blocks = [block.get_text(separator='. ')
              for block in
              soup.find_all('div', {'data-lyrics-container': True})
              ]
    return '\n'.join(blocks)


def song_lyrics(song_url):
    html = cached_get(song_url)
    return parse_lyrics(html)


def main(args):
    with open(args.outfile, 'w') as fp:
        iter = songs_for_artist(int(args.artist_id))
        json.dump(list(iter), fp)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('artist_id')
    p.add_argument('--outfile', default='out.txt')
    args = p.parse_args()
    main(args)
