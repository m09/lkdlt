from collections.abc import Iterable, Iterator

from sudachipy import Dictionary, SplitMode
from tatoebatools import ParallelCorpus

_tokenizer = Dictionary().create()


def _lemmas(string: str) -> str:
    return "#".join(
        f"{w.dictionary_form()}/{w.reading_form()}"
        for w in _tokenizer.tokenize(string, SplitMode.A)
    )


def load() -> list[tuple[str, str, str]]:
    ja_fr_corpus = ParallelCorpus("jpn", "fra")

    result = []
    for ja, fr in ja_fr_corpus:
        result.append((ja.text, fr.text, _lemmas(ja.text)))
    return result


def search(
    word: str, corpus: Iterable[tuple[str, str, str]]
) -> Iterator[tuple[str, str]]:
    lemmas = _lemmas(word)
    for ja, fr, example_lemmas in corpus:
        if lemmas in example_lemmas:
            yield ja, fr
