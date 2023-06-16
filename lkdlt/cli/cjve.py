from . import app


@app.command()
def cjve() -> None:
    from rich.progress import track

    from ..anki_connect import AnkiConnect
    from ..utils import common_prefix, common_suffix, is_kanji

    anki_connect = AnkiConnect()
    note_ids = anki_connect.find_notes('"deck:Core Japanese Vocabulary Extended"')
    note_infos = anki_connect.notes_info(note_ids)

    edited = 0
    for note_info in track(note_infos):
        kanji = anki_connect.get_field(note_info, "Expression")
        reading = anki_connect.get_field(note_info, "Reading")

        if "[" in reading:
            furigana = reading
        elif all(is_kanji(c) for c in kanji) and not any(is_kanji(c) for c in reading):
            furigana = f"{kanji}[{reading}]"
        else:
            prefix = common_prefix(kanji, reading)
            suffix = common_suffix(kanji, reading)
            middle_slice = slice(len(prefix), -len(suffix) if suffix else None)
            middle_kanji = kanji[middle_slice]
            middle_reading = reading[middle_slice]
            if all(is_kanji(c) for c in middle_kanji) and not any(
                is_kanji(c) for c in middle_reading
            ):
                furigana = (
                    f"{prefix}{' ' if prefix else ''}{middle_kanji}"
                    f"[{middle_reading}]{suffix}"
                )
            else:
                furigana = ""
        fields = {
            "Furigana": furigana,
        }
        edited += anki_connect.update_fields(note_info, fields)
    print(f"Edited {edited} notes")
