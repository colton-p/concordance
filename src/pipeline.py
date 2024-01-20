from collections import defaultdict, Counter
import dataclasses
import json
import re
import os.path
import time
from typing import List

import jinja2
import spacy
from spacy.tokens import Doc
from spacy.language import Language

import artist_defs

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = re.sub("\[.*?\]\.?", "", text)

    return text.translate(
        {
            0x2019: "'",
            0x2013: "-",
            0x2014: "-",
            0x0435: "e",
            0x2005: " ",
        }
    )

@dataclasses.dataclass
class Track:
    title: str
    album: str
    doc: Doc

    def to_json(self):
        return {
            "title": self.title,
            "album": self.album,
            "doc": self.doc.to_json(),
        }

    @staticmethod
    def from_json(data):
        return Track(
            title=data["title"],
            album=data["album"],
            doc=Doc(nlp.vocab).from_json(data["doc"]),
        )


def build_concordance(tracks: List[Track]):
    def good_tokens(tokens):
        for t in tokens:
            if not t.is_alpha:
                continue
            if t.is_stop:
                continue

            yield t

    conc = defaultdict(lambda: defaultdict(list))
    for track in tracks:
        for t in good_tokens(track.doc):
            conc[t.lemma_][track.title] += [t]

    return conc




def serialize(slug):
    def deco(func):
        def wrapper(artist, in_data, force=False):
            path = f"data/{slug}/{artist}.json"
            if not os.path.exists(path) or force:
                data = func(artist, in_data)
                with open(path, "w") as fp:
                    print(f"...write {len(data)} to {path}")
                    json.dump(data, fp, indent=2)
            else:
                print(f"...read from {path}")
                data = json.load(open(path))
            return data

        return wrapper

    return deco


@serialize("raw_lyrics")
def fetch(artist, in_data):
    fetch_func = artist_defs.ARTISTS[artist]["fetch"]
    return list(fetch_func())


@serialize("clean_lyrics")
def clean(artist, in_data):
    return [row | {"lyrics": clean_text(row["lyrics"])} for row in in_data]

@serialize("tokenized")
def tokenize(artist, in_data):
    @Language.component("ahh")
    def ahh(doc):
        for token in doc:
            if token.text == "Ahh":
                token.pos_ = "INTJ"
        return doc

    nlp.add_pipe("ahh", after="attribute_ruler")
    return [row | {"doc": nlp(row["lyrics"]).to_json()} for row in in_data]


def build_html(tracks, conc):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    tmpl = env.get_template("index.html")

    track_map = {t.title: t for t in tracks}

    def track_vars(word, track):
        tr = track_map[track]

        return {
            "title": tr.title,
            "album": tr.album,
            "uses": [
                {
                    "pos": occ.pos_,
                    "word": occ.text_with_ws,
                    "pre": "".join(
                        [t.text_with_ws for t in tr.doc[max(0, occ.i - 10) : occ.i]]
                    ),
                    "post": "".join(
                        [t.text_with_ws for t in tr.doc[occ.i + 1 : occ.i + 10]]
                    ),
                }
                for occ in conc[word][track]
            ],
        }

    def item_vars(word):
        tracks = conc[word]
        return {
            "word": word,
            "n_tracks": len(tracks),
            "n_uses": sum(len(occ) for occ in tracks.values()),
            "tracks": [track_vars(word, track) for track in tracks],
        }

    all_words = sorted(conc, key=lambda w: w.lower())
    conc = [item_vars(word) for word in all_words]

    album_words = defaultdict(Counter)
    for tr in tracks:
        album_words[tr.album] += Counter(t.text for t in tr.doc)

    album_counts = [
        {
            "name": album,
            "tracks": sum(1 for tr in tracks if tr.album == album),
            "words": sum(words.values()),
            "unique": len(words),
        }
        for (album, words) in album_words.items()
    ]
    album_counts += [
        {
            "name": "Total",
            "tracks": len(tracks),
            "words": sum(sum(c.values()) for c in album_words.values()),
            "unique": len(all_words),
        }
    ]

    letter_anchors = {}
    for word in all_words:
        char = word[0].lower()
        if char not in letter_anchors:
            letter_anchors[char] = word

    s = tmpl.render(conc=conc, album_counts=album_counts, letter_anchors=letter_anchors)

    with open("html/index.html", "w") as fp:
        fp.write(s)

def main(artist):
    print('main')
    force = False
    t0 = time.time()
    raw_lyrics = fetch(artist, None, force=False)
    print("fetch", time.time() - t0)

    t0 = time.time()
    raw_lyrics = [t for t in raw_lyrics if artist_defs.ARTISTS[artist]["filter"](t)]
    print("filter", time.time() - t0)

    t0 = time.time()
    clean_lyrics = clean(artist, raw_lyrics, force=force)
    print("clean", time.time() - t0)

    t0 = time.time()
    tracks = [Track.from_json(t) for t in tokenize(artist, clean_lyrics, force=force)]
    print("tokenize", time.time() - t0)

    t0 = time.time()
    conc = build_concordance(tracks)
    print("concordance", time.time() - t0)

    t0 = time.time()
    build_html(tracks, conc)
    print("html", time.time() - t0)


if __name__ == "__main__":
    main("taylor")
