from yaml import safe_load

from .config import config
from .model import KanjiInfo
from .stories import process_story_to_html


def load_kanji_infos(do_replacements: bool, do_stories: bool) -> list[KanjiInfo]:
    with config.paths.kanji.open(encoding="utf8") as fh:
        kanjis = safe_load(fh)
    kanjis_and_keywords = (
        (k["kanji"], k["original_keyword"] if "original_keyword" in k else k["keyword"])
        for k in kanjis
    )
    replacements = {k["kanji"]: k["keyword"] for k in kanjis if "original_keyword" in k}
    stories = {
        k["kanji"]: process_story_to_html(k["keyword"], k["story"])
        for k in kanjis
        if "story" in k
    }
    return KanjiInfo.from_data(
        kanjis_and_keywords,
        replacements if do_replacements else {},
        stories if do_stories else {},
    )
