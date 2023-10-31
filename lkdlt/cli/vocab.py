from . import app


@app.command()
def vocab() -> None:
    from pathlib import Path

    from rich.progress import track

    from ..anki_connect import AnkiConnect
    from ..config import config
    from ..furigana import Furigana, clean_empty_furigana, normalize_furigana
    from ..jmdict import JMDict
    from ..loading import load_kanji_infos
    from ..pronunciation import any_to_text, text_to_styled
    from ..utils import is_kanji

    kanji_infos = load_kanji_infos(do_replacements=True, do_stories=False)
    keywords = {kanji_info.kanji: kanji_info.keyword for kanji_info in kanji_infos}

    anki_connect = AnkiConnect()
    note_ids = anki_connect.find_notes(
        f'"deck:{config.vocab.deck_name}" "note:{config.vocab.model_name}"'
    )
    note_infos = anki_connect.notes_info(note_ids)

    jmdict = JMDict()
    jmdict.parse(Path.home() / "downloads" / "JMdict.gz")

    unknown_kanjis = set()
    edited = 0
    for note_info in track(note_infos):
        word = anki_connect.get_field(note_info, config.vocab.fields.word)
        meaning = anki_connect.get_field(note_info, config.vocab.fields.word_meaning)
        pronunciation = anki_connect.get_field(
            note_info, config.vocab.fields.pronunciation_text
        )
        pronunciation_text = any_to_text(pronunciation)
        pronunciation_styled = text_to_styled(pronunciation_text)
        word_furigana = Furigana(word)
        word_kanjis = []
        for character in word:
            if character in keywords:
                word_kanjis.append((character, keywords[character]))
            elif is_kanji(character) and character != "々":
                unknown_kanjis.add(character)
        kanji_keywords = config.vocab.keywords_join_string.join(
            config.vocab.keywords_format.format(kanji=kanji, keyword=keyword)
            for kanji, keyword in word_kanjis
        )
        fields = {
            config.vocab.fields.word: word_furigana.normalized,
            config.vocab.fields.word_kanji: word_furigana.kanji,
            config.vocab.fields.word_kana: word_furigana.kana,
            config.vocab.fields.example: normalize_furigana(
                clean_empty_furigana(
                    anki_connect.get_field(note_info, config.vocab.fields.example)
                )
            ),
            config.vocab.fields.kanji_keywords: kanji_keywords,
            config.vocab.fields.pronunciation_text: pronunciation_text,
            config.vocab.fields.pronunciation_styled: pronunciation_styled,
        }
        if not meaning:
            entries = jmdict.search(word_furigana.kanji, "fre")
            short = " ; ".join(e.short for e in entries if e.short is not None)
            extended = "\n———\n".join(
                e.extended for e in entries if e.extended is not None
            )
            if short:
                fields[config.vocab.fields.word_meaning] = short
            if extended:
                fields[config.vocab.fields.word_meaning_extended] = extended
        edited += anki_connect.update_fields(note_info, fields)
    print(f"Edited {edited} notes")
    if unknown_kanjis:
        print(f"Unknown kanjis: {' '.join(unknown_kanjis)}")
