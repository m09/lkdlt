from collections.abc import Iterable, Iterator
from io import StringIO
from itertools import zip_longest
from re import finditer, sub


def _normalize_text(pronunciation: str) -> str:
    return (
        pronunciation
        if "\\" not in pronunciation or "/" in pronunciation
        else f"/{pronunciation}"
    )


def _is_full_size(size: int) -> bool:
    match size:
        case 20:
            return True
        case 14:
            return False
        case _:
            raise ValueError("Expected character sizes are 14 and 20.")


def _extract_characters(svg: str) -> Iterator[tuple[str, bool]]:
    for match in finditer("<text.+?font-size:(.+?)px.+?>(.+?)</text>", svg):
        yield match.group(2), _is_full_size(int(match.group(1)))


def _merge_characters(
    characters: Iterable[str], are_full_size: Iterable[bool]
) -> tuple[str, ...]:
    buffer: list[str] = []
    result = []
    for character, full_size in zip(characters, are_full_size):
        if full_size and buffer:
            result.append("".join(buffer))
            buffer.clear()
        buffer.append(character)
    if buffer:
        result.append("".join(buffer))
    return tuple(result)


def _is_low_pitch(cy: int) -> bool:
    match cy:
        case 30:
            return True
        case 5:
            return False
        case _:
            raise ValueError("Expected cy values are 30 and 5.")


def _extract_low_pitches(svg: str) -> Iterator[bool]:
    for match in finditer('<circle.*? cy="(.+?)"', svg):
        yield _is_low_pitch(int(match.group(1)))


def _svg_to_text(pronunciation: str) -> str:
    characters = _merge_characters(*zip(*_extract_characters(pronunciation)))
    low_pitches = list(_extract_low_pitches(pronunciation))[:-1]
    current_low_pitch = True
    result = []
    for low_pitch, character in zip_longest(low_pitches, characters):
        if current_low_pitch and not low_pitch:
            result.append("/")
        elif not current_low_pitch and low_pitch:
            result.append("\\")
        if character is not None:
            result.append(character)
        current_low_pitch = low_pitch

    return "".join(result)


def _akebi_to_text(pronunciation: str) -> str:
    pronunciation = sub('<u class="low-pitch">(.*?)</u>', r"\1", pronunciation)
    pronunciation = sub('<b class="high-pitch">(.*?)</b>', r"/\1\\", pronunciation)
    pronunciation = sub(
        '<b class="high-pitch-unterminated">(.*?)</b>', r"/\1", pronunciation
    )
    return pronunciation


def _dispatch_to_converter(pronunciation: str) -> str:
    if "<svg" in pronunciation:
        return _svg_to_text(pronunciation)
    elif (
        'class="low-pitch"' in pronunciation
        or 'class="high-pitch"' in pronunciation
        or 'class="high-pitch-unterminated"' in pronunciation
    ):
        return _akebi_to_text(pronunciation)
    else:
        return _normalize_text(pronunciation)


def any_to_text(pronunciation: str) -> str:
    return _dispatch_to_converter(pronunciation)


def text_to_styled(pronunciation: str) -> str:
    buffer: list[str] = []
    low = True
    first, second, third = "", "", ""
    for c in pronunciation:
        match c:
            case "/":
                low = False
                first = "".join(buffer)
                buffer.clear()
            case "\\":
                low = True
                second = "".join(buffer)
                buffer.clear()
            case _:
                buffer.append(c)
    if low:
        third = "".join(buffer)
    else:
        second = "".join(buffer)

    with StringIO() as sio:
        if first:
            sio.write(f'<span class="low-pitch">{first}</span>')
        if second:
            if third:
                sio.write(f'<span class="high-pitch">{second}</span>')
            else:
                sio.write(f'<span class="high-pitch-unterminated">{second}</span>')
        if third:
            sio.write(f'<span class="low-pitch">{third}</span>')
        return sio.getvalue()
