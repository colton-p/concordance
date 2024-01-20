from extraction import genius as g
from extraction import dylan


def filter_taylor(track):
    keep = [
        'Taylor Swift',
        "Fearless (Taylor\u2019s Version)",
        "Speak Now (Taylor\u2019s Version)",
        "Red (Taylor\u2019s Version)",
        "1989 (Taylor\u2019s Version)",
        "reputation",
        "Lover",
        "folklore",
        "evermore",
        "Midnights",
        "Midnights (3am Edition)",
    ]
    if 'voice memo' in track['title'].lower(): return False
    if track['album'] not in keep: return False
    return True


ARTISTS = {
    "taylor": {
        'fetch': lambda: g.songs_for_artist(1177),
        'filter': filter_taylor,
    },
    "dylan": {
        'fetch': dylan.all_tracks,
        'filter': lambda x: 'Bob Dylan' in x['credit']
    },
}