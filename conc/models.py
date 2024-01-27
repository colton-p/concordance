from typing import NamedTuple

from spacy.tokens import Doc


class Track(NamedTuple):
    title: str
    album: str
    lyrics: str

    def to_json(self):
        return {"title": self.title, "album": self.album, "lyrics": self.lyrics}


class TokenTrack(NamedTuple):
    title: str
    album: str
    doc: Doc

    def to_json(self):
        return {"title": self.title, "album": self.album, "doc": self.doc.to_json()}

    @staticmethod
    def from_json(nlp, data):
        return TokenTrack(
            title=data["title"],
            album=data["album"],
            doc=Doc(nlp.vocab).from_json(data["doc"]),
        )
