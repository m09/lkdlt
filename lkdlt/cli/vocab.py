from rich.progress import track

from ..anki_connect import AnkiConnect
from ..config import config
from ..loading import load_kanji_infos
from ..utils import is_kanji
from . import app


@app.command()
def vocab() -> None:
    anki_connect = AnkiConnect()
    kanji_infos = load_kanji_infos(do_replacements=True, do_stories=False)
    keywords = {kanji_info.kanji: kanji_info.keyword for kanji_info in kanji_infos}
    note_ids = anki_connect.find_notes(
        f'"deck:{config.vocab_deck_name}" "note:{config.vocab_word_model_name}"'
    )
    note_infos = anki_connect.notes_info(note_ids)

    modified = 0
    added = 0
    unknown = []
    for note_info in track(note_infos):
        current_kanji_keywords = note_info["fields"][config.vocab_kanji_keywords_field][
            "value"
        ]
        word = note_info["fields"][config.vocab_word_field]["value"]
        word_kanjis = []
        for character in word:
            if character in keywords:
                word_kanjis.append((character, keywords[character]))
            elif is_kanji(character):
                unknown.append(character)
        kanji_keywords = " ⋅ ".join(
            config.vocab_keywords_format.format(kanji=kanji, keyword=keyword)
            for kanji, keyword in word_kanjis
        )
        fields = {config.vocab_kanji_keywords_field: kanji_keywords}
        if kanji_keywords != current_kanji_keywords:
            if not current_kanji_keywords:
                added += 1
            else:
                modified += 1
            anki_connect.update_note_fields(note_info["noteId"], fields)

    if unknown:
        print(f"No keyword found for {len(unknown)} kanjis: {', '.join(unknown)}.")
    print(f"Added {added} keywords, modified {modified} keywords.")
