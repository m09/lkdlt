from typing import Optional

from typer import Argument

from . import app


@app.command()
def deck(limit: Optional[int] = Argument(None)) -> None:  # noqa: B008
    from collections import defaultdict
    from itertools import islice

    from rich.progress import track

    from ..anki_connect import AnkiConnect
    from ..config import config
    from ..furigana import furigana_to_ruby
    from ..kanjidic import parse
    from ..loading import load_kanji_infos
    from ..utils import is_kanji

    kanjis = parse()
    anki_connect = AnkiConnect()
    note_ids = anki_connect.find_notes(f'"deck:{config.kanji.deck_name}"')
    note_infos = anki_connect.notes_info(note_ids)
    kanji_to_note_infos = {
        n["fields"][config.kanji.fields.kanji]["value"]: n for n in note_infos
    }

    word_note_ids = anki_connect.find_notes(
        f'"deck:{config.vocab.deck_name}" "note:{config.vocab.model_name}" -is:new'
    )
    word_note_infos = anki_connect.notes_info(word_note_ids)
    kanji_to_words = defaultdict(set)
    for word_note_info in word_note_infos:
        word = word_note_info["fields"][config.vocab.fields.word]["value"]
        for character in word:
            if is_kanji(character):
                kanji_to_words[character].add(
                    (
                        word,
                        word_note_info["fields"][config.vocab.fields.word_meaning][
                            "value"
                        ],
                    )
                )

    modified = 0
    added = 0
    unknown = []
    kanji_infos = load_kanji_infos(do_replacements=True, do_stories=True)
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
        words = "\n".join(
            f'<tr><td class="word">{furigana_to_ruby(word)}</td>'
            f'<td class="meaning">{meaning}</td></tr>'
            for word, meaning in sorted(kanji_to_words[kanji_info.kanji])[:5]
        )
        if words:
            words = f'<table class="words">{words}</table>'
        try:
            on = kanjis[kanji_info.kanji].on[0]
        except (IndexError, KeyError):
            on = ""
        fields = {
            config.kanji.fields.keyword: kanji_info.keyword,
            config.kanji.fields.kanji: kanji_info.kanji,
            config.kanji.fields.words: words,
            config.kanji.fields.svg_found: svg_found,
            config.kanji.fields.svg: svg,
            config.kanji.fields.story: kanji_info.story,
            config.kanji.fields.identifier: str(kanji_info.identifier),
            config.kanji.fields.on_pronunciation: on,
            config.kanji.fields.furigana: f"{kanji_info.kanji}[{on}]",
        }
        if kanji_info.kanji in kanji_to_note_infos:
            note_info = kanji_to_note_infos[kanji_info.kanji]
            anki_fields = {k: v["value"] for k, v in note_info["fields"].items()}
            if anki_fields != fields:
                modified += 1
                anki_connect.update_fields(note_info, fields)
        else:
            added += 1
            anki_connect.add_note(
                config.kanji.deck_name, config.kanji.model_name, fields
            )
    if unknown:
        print(f"No SVG found for {', '.join(unknown)}.")
    print(f"Added {added} notes, modified {modified} notes.")
