from collections import defaultdict

from ..loading import load_kanji_infos
from . import app


@app.command()
def stats() -> None:
    keywords = defaultdict(set)

    for kanji_info in load_kanji_infos(should_replace=False):
        keywords[kanji_info.keyword].add(kanji_info.kanji)

    for keyword, kanjis in keywords.items():
        if len(kanjis) > 1:
            print(keyword, " ⋅ ".join(kanjis))
