from collections import defaultdict
import re
from typing import Dict, List

import spacy
from spacy.tokens import Doc, Token

from models import TokenTrack
from util import phase

nlp = spacy.load("en_core_web_sm")


def build_concordance(tracks: List[TokenTrack]) -> Dict[str, Dict[str, List[Token]]]:
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

    return dict(conc)


class OutputBuilder:
    def __init__(self, tracks: List[TokenTrack]) -> None:
        self.tracks = tracks
        self.track_map = {t.title: t for t in tracks}
        self.conc = build_concordance(tracks)

    def output(self):
        all_words = sorted(self.conc, key=lambda w: w.lower())
        return [self.entry(word) for word in all_words]

    def entry(self, word: str):
        tracks = self.conc[word]
        return {
            "word": word,
            "tracks": [
                self.track(self.track_map[track_name], occs)
                for (track_name, occs) in tracks.items()
            ],
        }

    def track(self, track: TokenTrack, occs: List[Token]):
        return {
            "title": track.title,
            "album": track.album,
            "usages": [self.usage(track, occ) for occ in occs],
        }

    def usage(self, track: TokenTrack, occ: Token):
        doc = track.doc
        return {
            "pos": occ.pos_,
            "word": occ.text,
            # "pre": "".join([t.text_with_ws for t in doc[max(0, occ.i - 10) : occ.i]]),
            # "post": "".join([t.text_with_ws for t in doc[occ.i + 1 : occ.i + 10]]),
            "pre": self.context(doc, occ.i, -10),
            "post": self.context(doc, occ.i, +10),
        }

    def context(self, doc: Doc, ix: int, offset: int):
        if offset > 0:
            (start, end) = ix + 1, ix + offset
            strip_pat = r'\W+$'
        else:
            (start, end) = max(0, ix + offset), ix
            strip_pat = r'^\W+'

        text = "".join(t.text_with_ws for t in doc[start:end])

        return re.sub(strip_pat, '', text)


def concord(_artist, in_data: List[TokenTrack]):
    builder = OutputBuilder(in_data)
    return builder.output()


if __name__ == "__main__":

    def build(**kwargs):
        return TokenTrack.from_json(nlp, kwargs)

    phase(concord, build)
