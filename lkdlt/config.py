from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load

from .paths import config_path


class Config(BaseModel):
    animcjk_dir: Path
    kanji_path: Path
    edits_path: Path
    stories_path: Path
    deck_name: str
    model_name: str
    keyword_field: str
    kanji_field: str
    svg_found_field: str
    svg_field: str
    story_field: str
    identifier_field: str

    @classmethod
    def load(cls) -> "Config":
        with config_path.open(encoding="utf8") as fh:
            obj = safe_load(fh)
        return Config.parse_obj(obj)
