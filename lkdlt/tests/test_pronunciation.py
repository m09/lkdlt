from importlib.resources import as_file, files
from typing import Any

from pytest import mark

from lkdlt.pronunciation import any_to_text, text_to_styled


@mark.parametrize(
    "text, styled",
    [
        (
            "し/んげん",
            '<span class="low-pitch">し</span>'
            '<span class="high-pitch-unterminated">んげん</span>',
        ),
        (
            "し/な\\んやく",
            '<span class="low-pitch">し</span>'
            '<span class="high-pitch">な</span>'
            '<span class="low-pitch">んやく</span>',
        ),
        (
            "/か\\んしゃ",
            '<span class="high-pitch">か</span><span class="low-pitch">んしゃ</span>',
        ),
        (
            "/かんしゃ",
            '<span class="high-pitch-unterminated">かんしゃ</span>',
        ),
        (
            "かんしゃ",
            '<span class="low-pitch">かんしゃ</span>',
        ),
    ],
)
def test_text_to_styled(text: str, styled: str) -> None:
    assert text_to_styled(text) == styled


def test_text_to_styled_empty() -> None:
    assert text_to_styled("") == ""


@mark.parametrize(
    "akebi, text",
    [
        (
            '<u class="low-pitch">し</u><b class="high-pitch-unterminated">んげん</b>',
            "し/んげん",
        ),
        (
            '<u class="low-pitch">し</u>'
            '<b class="high-pitch">な</b>'
            '<u class="low-pitch">んやく</u>',
            "し/な\\んやく",
        ),
        (
            '<b class="high-pitch">か</b><u class="low-pitch">んしゃ</u>',
            "/か\\んしゃ",
        ),
        (
            '<b class="high-pitch-unterminated">かんしゃ</b>',
            "/かんしゃ",
        ),
        (
            '<u class="low-pitch">かんしゃ</u>',
            "かんしゃ",
        ),
    ],
)
def test_akebi_to_raw(akebi: str, text: str) -> None:
    assert any_to_text(akebi) == text


def pytest_generate_tests(metafunc: Any) -> None:
    if "svg" in metafunc.fixturenames and "text" in metafunc.fixturenames:
        svgs_and_texts = []
        for f in files("lkdlt.tests.pronunciation_data").iterdir():
            if f.name.endswith(".txt"):
                with as_file(f) as fh:
                    text, svg, *_ = fh.read_text(encoding="utf8").split("\n")
                    svgs_and_texts.append((svg, text))
        metafunc.parametrize("svg, text", svgs_and_texts)


def test_svg_to_raw(svg: str, text: str) -> None:
    assert any_to_text(svg) == text


def test_any_to_text_empty() -> None:
    assert any_to_text("") == ""
