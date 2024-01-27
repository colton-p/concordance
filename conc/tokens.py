from typing import List

import spacy
from spacy.language import Language

from models import Track, TokenTrack
from util import phase

nlp = spacy.load("en_core_web_sm")


def tokenize(_artist, in_data: List[Track]):
    @Language.component("ahh")
    def ahh(doc):
        for token in doc:
            if token.text == "Ahh":
                token.pos_ = "INTJ"
        return doc

    nlp.add_pipe("ahh", after="attribute_ruler")
    return [
        TokenTrack(
            title=row.title,
            album=row.album,
            doc=nlp(row.lyrics),
        ) for row in in_data]


if __name__ == "__main__":
    phase(tokenize, Track)
