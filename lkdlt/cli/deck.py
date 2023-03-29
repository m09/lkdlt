from itertools import islice
from typing import Optional

from rich.progress import track
from typer import Argument

from ..anki_connect import AnkiConnect
from ..config import Config
from ..loading import load_kanji_infos
from . import app


@app.command()
def deck(limit: Optional[int] = Argument(None)) -> None:  # noqa: B008
    config = Config.load()
    anki_connect = AnkiConnect()
    note_ids = anki_connect.find_notes(f'"deck:{config.deck_name}"')
    note_infos = anki_connect.notes_info(note_ids)
    kanji_to_note_infos = {
        n["fields"][config.kanji_field]["value"]: n for n in note_infos
    }

    modified = 0
    added = 0
    unknown = []
    kanji_infos = load_kanji_infos(config=config, do_replacements=True, do_stories=True)
    for kanji_info in track(
        islice(kanji_infos, limit), total=limit or len(kanji_infos)
    ):
        if kanji_info.svg is None:
            unknown.append(kanji_info.kanji)
            svg = ""
            svg_found = ""
        else:
            svg = kanji_info.svg
            svg_found = "Oui"
        fields = {
            config.keyword_field: kanji_info.keyword,
            config.kanji_field: kanji_info.kanji,
            config.svg_found_field: svg_found,
            config.svg_field: svg,
            config.story_field: kanji_info.story,
            config.identifier_field: str(kanji_info.identifier),
        }
        if kanji_info.kanji in kanji_to_note_infos:
            note_info = kanji_to_note_infos[kanji_info.kanji]
            anki_fields = {k: v["value"] for k, v in note_info["fields"].items()}
            if anki_fields != fields:
                modified += 1
                anki_connect.update_note_fields(note_info["noteId"], fields)
        else:
            added += 1
            anki_connect.add_note(config.deck_name, config.model_name, fields)
    if unknown:
        print(f"No SVG found for {', '.join(unknown)}.")
    print(f"Added {added} notes, modified {modified} notes.")
