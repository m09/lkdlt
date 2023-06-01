from . import app


@app.command()
def vocab() -> None:
    from rich.progress import track

    from ..anki_connect import AnkiConnect
    from ..config import config
    from ..furigana import Furigana, clean_empty_furigana, normalize_furigana
    from ..loading import load_kanji_infos
    from ..utils import is_kanji

    kanji_infos = load_kanji_infos(do_replacements=True, do_stories=False)
    keywords = {kanji_info.kanji: kanji_info.keyword for kanji_info in kanji_infos}

    anki_connect = AnkiConnect()
    note_ids = anki_connect.find_notes(
        f'"deck:{config.vocab_deck_name}" "note:{config.vocab_word_model_name}"'
    )
    note_infos = anki_connect.notes_info(note_ids)

    unknown_kanjis = set()
    edited = 0
    for note_info in track(note_infos):
        word = anki_connect.get_field(note_info, config.vocab_word_field)
        word_furigana = Furigana(word)
        word_kanjis = []
        for character in word:
            if character in keywords:
                word_kanjis.append((character, keywords[character]))
            elif is_kanji(character):
                unknown_kanjis.add(character)
        kanji_keywords = config.vocab_keywords_join_string.join(
            config.vocab_keywords_format.format(kanji=kanji, keyword=keyword)
            for kanji, keyword in word_kanjis
        )
        fields = {
            config.vocab_word_field: word_furigana.normalized,
            config.vocab_word_kanji_field: word_furigana.kanji,
            config.vocab_word_kana_field: word_furigana.kana,
            config.vocab_word_kanji_kana_field: word_furigana.kanji
            + word_furigana.kana,
            config.vocab_example_field: normalize_furigana(
                clean_empty_furigana(
                    anki_connect.get_field(note_info, config.vocab_example_field)
                )
            ),
            config.vocab_kanji_keywords_field: kanji_keywords,
        }
        edited += anki_connect.update_fields(note_info, fields)
    print(f"Edited {edited} notes")
    if unknown_kanjis:
        print(f"Unknown kanjis: {' '.join(unknown_kanjis)}")
