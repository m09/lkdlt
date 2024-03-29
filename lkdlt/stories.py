from re import IGNORECASE
from re import compile as re_compile
from re import escape, sub

_component_pattern = re_compile(r"\*([^*]+)\*")
_keyword_pattern = re_compile(r"#([^#]+)#")
_ref_pattern = re_compile(r"\{([^{}]+)\}")


def process_story_to_html(keyword: str, story: str) -> str:
    story = _component_pattern.sub(r'<span class="composant">\1</span>', story)
    story = _ref_pattern.sub(r"(\1)", story)
    new_story = _keyword_pattern.sub(r'<span class="motclef">\1</span>', story)
    story = (
        sub(
            rf"\b{escape(keyword)}\b",
            f'<span class="motclef">{keyword}</span>',
            story,
            flags=IGNORECASE,
        )
        if new_story == story
        else new_story
    )
    return story
