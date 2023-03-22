from collections import defaultdict

from ..config import Config
from ..loading import load_kanji_infos
from . import app


@app.command()
def stats() -> None:
    config = Config.load()
    kanji_infos = load_kanji_infos(config, do_replacements=False, do_stories=False)
    keywords = defaultdict(set)

    for kanji_info in kanji_infos:
        keywords[kanji_info.keyword].add(kanji_info.kanji)

    for keyword, kanjis in keywords.items():
        if len(kanjis) > 1:
            print(keyword, " ⋅ ".join(kanjis))
