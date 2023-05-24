from . import app


@app.command()
def vocab() -> None:
    from rich.progress import track

    from ..anki_connect import AnkiConnect
    from ..config import config
    from ..furigana import furigana_to_kana, furigana_to_kanji
    from ..loading import load_kanji_infos
    from ..utils import Stats, is_kanji

    kanji_infos = load_kanji_infos(do_replacements=True, do_stories=False)
    keywords = {kanji_info.kanji: kanji_info.keyword for kanji_info in kanji_infos}

    anki_connect = AnkiConnect()
    note_ids = anki_connect.find_notes(
        f'"deck:{config.vocab_deck_name}" "note:{config.vocab_word_model_name}"'
    )
    note_infos = anki_connect.notes_info(note_ids)

    keywords_stats = Stats("keywords")
    kana_stats = Stats("kana")
    kanji_stats = Stats("kanji")
    for note_info in track(note_infos):
        word = note_info["fields"][config.vocab_word_field]["value"]
        anki_connect.update_field_with_stats(
            note_info, config.vocab_word_kana_field, furigana_to_kana(word), kana_stats
        )
        anki_connect.update_field_with_stats(
            note_info,
            config.vocab_word_kanji_field,
            furigana_to_kanji(word),
            kanji_stats,
        )
        word_kanjis = []
        for character in word:
            if character in keywords:
                word_kanjis.append((character, keywords[character]))
            elif is_kanji(character):
                keywords_stats.unknown.add(character)
        kanji_keywords = " ⋅ ".join(
            config.vocab_keywords_format.format(kanji=kanji, keyword=keyword)
            for kanji, keyword in word_kanjis
        )
        anki_connect.update_field_with_stats(
            note_info,
            config.vocab_kanji_keywords_field,
            kanji_keywords,
            keywords_stats,
        )

    print(keywords_stats)
    print(kana_stats)
    print(kanji_stats)
