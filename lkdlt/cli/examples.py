from . import app


@app.command()
def examples() -> None:
    from random import sample

    from rich.console import Console
    from typer import Exit

    from ..anki_connect import AnkiConnect
    from ..config import config
    from ..examples import load, search

    corpus = load()
    console = Console()
    anki_connect = AnkiConnect()
    note_ids = anki_connect.find_notes(
        f'"deck:{config.vocab.deck_name}" "note:{config.vocab.model_name}"'
    )
    note_infos = anki_connect.notes_info(note_ids)

    no_example_words = set()
    edited = 0
    for note_info in note_infos:
        if anki_connect.get_field(note_info, config.vocab.fields.example):
            continue
        word = anki_connect.get_field(note_info, config.vocab.fields.word_kanji)
        kana = anki_connect.get_field(note_info, config.vocab.fields.word_kana)
        meaning = anki_connect.get_field(note_info, config.vocab.fields.word_meaning)
        results = list(search(word, corpus))
        if not results:
            no_example_words.add(word)
            console.print(f"Could not find an example for word {word}")
            continue

        selected = None
        n_options = min(len(results), 5)
        random_examples = sample(results, k=n_options)
        console.print(
            f"[bold]Examples ({n_options}/{len(results)}) "
            f"for word {word} ⋅ {kana} ⋅ {meaning})[/]"
        )
        while selected is None:
            for i, (ja, fr) in enumerate(random_examples, start=1):
                console.print(f"{i}. {ja}\n   {fr}")
            answer = input(
                "# Enter the number of the example you want to pick, r to resample, "
                "q to quit\n> "
            )
            match answer:
                case "q":
                    raise Exit()
                case "r":
                    random_examples = sample(results, k=n_options)
                case _ if 0 < int(answer) <= n_options:
                    selected = int(answer) - 1
                case _:
                    "# Could not parse the provided input, trying again."

        print(selected)
        ja, fr = results[selected]

        fields = {
            config.vocab.fields.example: ja,
            config.vocab.fields.example_translation: fr,
        }
        edited += anki_connect.update_fields(note_info, fields)
    print(f"Edited {edited} notes")
    if no_example_words:
        print(f"Words with no example: {' '.join(no_example_words)}")
