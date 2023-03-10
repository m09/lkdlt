from re import compile as re_compile
from re import sub

_component_pattern = re_compile(r"\*([^*]+)\*")
_keyword_pattern = re_compile(r"#([^#]+)#")
_ref_pattern = re_compile(r"\{([^{}]+)\}")


def process_story_to_html(keyword: str, story: str) -> str:
    story = _component_pattern.sub(r"<i>\1</i>", story)
    story = _ref_pattern.sub(r"(\1)", story)
    story = sub(rf"\b{keyword}\b", f"<b>{keyword}</b>", story)
    story = _keyword_pattern.sub(r"<b>\1</b>", story)
    return story
