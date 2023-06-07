from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load

from .paths import config_path


class _VocabFields(BaseModel):
    kanji_keywords: str
    word: str
    word_meaning: str
    word_kana: str
    word_kanji: str
    word_kanji_kana: str
    example: str
    pronunciation_text: str
    pronunciation_styled: str


class _Vocab(BaseModel):
    deck_name: str
    model_name: str
    keywords_format: str
    keywords_join_string: str
    fields: _VocabFields


class _KanjiFields(BaseModel):
    keyword: str
    on_pronunciation: str
    furigana: str
    kanji: str
    words: str
    svg_found: str
    svg: str
    story: str
    identifier: str


class _Kanji(BaseModel):
    deck_name: str
    model_name: str
    fields: _KanjiFields


class _Paths(BaseModel):
    animcjk: Path
    kanji: Path
    edits: Path
    stories: Path
    kanjidic: Path


class _Config(BaseModel):
    paths: _Paths
    kanji: _Kanji
    vocab: _Vocab

    @classmethod
    def load(cls) -> "_Config":
        with config_path.open(encoding="utf8") as fh:
            obj = safe_load(fh)
        return _Config.parse_obj(obj)


config = _Config.load()
