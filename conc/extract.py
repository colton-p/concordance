import argparse
import json

from extraction import genius as g
from extraction import dylan

EXTRACTORS = {
    'taylor': lambda: g.songs_for_artist(1177),
    'fiona': lambda: g.songs_for_artist(653),
    'dylan': lambda: dylan.all_tracks,
}

def extract(artist, _):
    extractor = EXTRACTORS[artist]
    return [e for e in extractor()]


def main(args):
    with open(args.outfile, 'w', encoding='utf8') as fp:

        print(f'extract {args.artist}...')
        data = extract(args.artist, None)
        print(f'... got {len(data)} records')

        json.dump(data, fp, indent=2)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("artist", choices=EXTRACTORS.keys())
    p.add_argument("--outfile", default="out.json")

    main(p.parse_args())
