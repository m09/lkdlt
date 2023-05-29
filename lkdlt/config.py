from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load

from .paths import config_path


class _Config(BaseModel):
    animcjk_dir: Path
    kanji_path: Path
    edits_path: Path
    stories_path: Path
    kanji_dic_path: str
    kanji_deck_name: str
    kanji_model_name: str
    kanji_keyword_field: str
    kanji_kanji_field: str
    kanji_words_field: str
    kanji_svg_found_field: str
    kanji_svg_field: str
    kanji_story_field: str
    kanji_identifier_field: str
    vocab_deck_name: str
    vocab_kanji_keywords_field: str
    vocab_word_field: str
    vocab_word_meaning_field: str
    vocab_word_kana_field: str
    vocab_word_kanji_field: str
    vocab_word_model_name: str
    vocab_example_field: str
    vocab_keywords_format: str

    @classmethod
    def load(cls) -> "_Config":
        with config_path.open(encoding="utf8") as fh:
            obj = safe_load(fh)
        return _Config.parse_obj(obj)


config = _Config.load()
