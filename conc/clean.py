import re
from typing import List

from models import Track
from util import phase


class Cleaner:
    @staticmethod
    def for_artist(artist):
        if artist == 'taylor':
            return Taylor
        return Cleaner

    @staticmethod
    def filter(_track: Track):
        return True

    @staticmethod
    def clean_text(text):
        text = re.sub(r"\[.*?\]\.?", "", text)

        return text.translate(
            {
                0x2019: "'",
                0x2013: "-",
                0x2014: "-",
                0x0435: "e",
                0x2005: " ",
            }
        ).strip()

class Taylor(Cleaner):
    @staticmethod
    def filter(track: Track):
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
        if 'voice memo' in track.title.lower():
            return False
        if track.album not in keep:
            return False
        return True

def clean_track(cleaner, track: Track):
    return Track(
        **(track._asdict() | {'lyrics': cleaner.clean_text(track.lyrics)})
    )

def clean(artist, in_data: List[Track]):
    cleaner = Cleaner.for_artist(artist)

    return [
        clean_track(cleaner, row)
        for row in in_data
        if cleaner.filter(row)
    ]

if __name__ == "__main__":
    phase(clean, Track)
