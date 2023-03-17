from ..loading import load_kanji_infos
from . import app


@app.command()
def index() -> None:
    for kanji_info in load_kanji_infos():
        print(f"{kanji_info.kanji}\t{kanji_info.keyword}")
