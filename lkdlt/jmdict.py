from collections import defaultdict
from dataclasses import dataclass
from gzip import open as gzip_open
from pathlib import Path

from lxml.etree import Element, iterparse

_xml = "{http://www.w3.org/XML/1998/namespace}"


def _first_maybe(element: Element, attr: str) -> str | None:
    return element.findtext(attr)


def _first(element: Element, attr: str) -> str:
    return element.findtext(attr)


def _list(element: Element, attr: str) -> list[str]:
    return [e.text for e in element.findall(attr)]


def _attrib_maybe(element: Element, attr: str) -> str | None:
    return element.get(attr)


def _attrib(element: Element, attr: str, default: str) -> str:
    return element.get(attr) or default


@dataclass
class REle:
    reb: str
    re_nokanji: str | None
    re_restr: list[str]
    re_inf: list[str]
    re_pri: list[str]

    @classmethod
    def from_etree(cls, element: Element) -> "REle":
        return cls(
            reb=_first(element, "reb"),
            re_nokanji=_first_maybe(element, "re_nokanji"),
            re_restr=_list(element, "re_restr"),
            re_inf=_list(element, "re_inf"),
            re_pri=_list(element, "re_pri"),
        )


@dataclass
class KEle:
    keb: str
    ke_infs: list[str]
    ke_pris: list[str]

    @classmethod
    def from_etree(cls, element: Element) -> "KEle":
        return cls(
            keb=_first(element, "keb"),
            ke_infs=_list(element, "ke_inf"),
            ke_pris=_list(element, "ke_pri"),
        )


@dataclass
class LSource:
    value: str
    lang: str
    ls_type: str

    @classmethod
    def from_etree(cls, element: Element) -> "LSource":
        return cls(
            value=element.text,
            lang=_attrib(element, f"{_xml}lang", "eng"),
            ls_type=_attrib(element, "ls_type", "full"),
        )


@dataclass
class Gloss:
    value: str
    pri: bool
    g_type: str | None = None
    g_gend: str | None = None

    @classmethod
    def from_etree(cls, element: Element) -> tuple[str, "Gloss"]:
        return _attrib(element, f"{_xml}lang", "eng"), cls(
            value=element.findtext("pri") or element.text,
            pri=bool(element.find("pri")),
            g_type=_attrib_maybe(element, "g_type"),
            g_gend=_attrib_maybe(element, "g_gend"),
        )


@dataclass
class ExSrce:
    value: str
    type: str | None

    @classmethod
    def from_etree(cls, element: Element) -> "ExSrce":
        return ExSrce(element.text, element.get("exsrc_type"))


@dataclass
class Example:
    ex_srce: ExSrce
    ex_text: str
    ex_sent: dict[str, tuple[str, ...]]

    @classmethod
    def from_etree(cls, element: Element) -> "Example":
        ex_sents = defaultdict(list)
        for e in element.findall("ex_sent"):
            ex_sents[_attrib(e, f"{_xml}lang", "eng")] = e.text
        return cls(
            ex_srce=ExSrce.from_etree(element.find("ex_srce")),
            ex_text=element.findtext("ex_text"),
            ex_sent={k: tuple(v) for k, v in ex_sents.items()},
        )


@dataclass
class Sense:
    stagk: list[str]
    stagr: list[str]
    pos: list[str]
    xref: list[str]
    ant: list[str]
    field: list[str]
    misc: list[str]
    s_inf: list[str]
    dial: list[str]
    lsource: list[LSource]
    gloss: dict[str, tuple[Gloss, ...]]
    example: list[Example]

    @classmethod
    def from_etree(cls, element: Element) -> "Sense":
        glosses_list = [Gloss.from_etree(e) for e in element.findall("gloss")]
        glosses = defaultdict(list)
        for lang, gloss in glosses_list:
            glosses[lang].append(gloss)

        return Sense(
            stagk=_list(element, "stagk"),
            stagr=_list(element, "stagr"),
            pos=_list(element, "pos"),
            xref=_list(element, "xref"),
            ant=_list(element, "ant"),
            field=_list(element, "field"),
            misc=_list(element, "misc"),
            s_inf=_list(element, "s_inf"),
            dial=_list(element, "dial"),
            lsource=[LSource.from_etree(e) for e in element.findall("lsource")],
            gloss={k: tuple(v) for k, v in glosses.items()},
            example=[Example.from_etree(e) for e in element.findall("example")],
        )


@dataclass
class Entry:
    ent_seq: int
    k_eles: list[KEle]
    r_eles: list[REle]
    senses: list[Sense]

    @classmethod
    def from_etree(cls, element: Element) -> "Entry":
        return cls(
            ent_seq=int(_first(element, "ent_seq")),
            k_eles=[KEle.from_etree(e) for e in element.findall("k_ele")],
            r_eles=[REle.from_etree(e) for e in element.findall("r_ele")],
            senses=[Sense.from_etree(e) for e in element.findall("sense")],
        )

    def definition(self, lang: str) -> str | None:
        for sense in (s for s in self.senses if lang in s.gloss):
            if lang not in sense.gloss:
                pass
        return None


@dataclass
class Definition:
    senses: tuple[tuple[str, ...], ...]
    pos: tuple[tuple[str, ...], ...]

    @property
    def extended(self) -> str | None:
        return (
            "\n".join(
                f"{i}. {', '.join(s)}" for i, s in enumerate(self.senses, start=1)
            )
            or None
        )

    @property
    def short(self, n: int = 3) -> str | None:
        if self.senses:
            return ", ".join(gloss for gloss, _ in zip(self.senses[0], range(n)))
        else:
            return None

    @classmethod
    def from_entry(cls, entry: Entry, lang: str) -> "Definition":
        senses = []
        pos = []
        for sense in entry.senses:
            if lang in sense.gloss:
                senses.append(tuple(g.value for g in sense.gloss[lang]))
                pos.append(tuple(sense.pos))
        return cls(tuple(senses), tuple(pos))


class JMDict:
    def __init__(self) -> None:
        self._kanjis: dict[str, list[Entry]] = {}
        self._readings: dict[str, list[Entry]] = {}

    def parse(self, path: Path) -> None:
        with gzip_open(path) as fh:
            for _, element in iterparse(fh, tag="entry"):
                entry = Entry.from_etree(element)
                for k_ele in entry.k_eles:
                    if k_ele.keb not in self._kanjis:
                        self._kanjis[k_ele.keb] = []
                    self._kanjis[k_ele.keb].append(entry)
                for r_ele in entry.r_eles:
                    if r_ele.reb not in self._readings:
                        self._readings[r_ele.reb] = []
                    self._readings[r_ele.reb].append(entry)
                element.clear(keep_tail=True)

    def search(self, string: str, lang: str) -> tuple[Definition, ...]:
        if string in self._kanjis:
            return tuple(Definition.from_entry(e, lang) for e in self._kanjis[string])
        if string in self._readings:
            return tuple(Definition.from_entry(e, lang) for e in self._readings[string])
        return ()
