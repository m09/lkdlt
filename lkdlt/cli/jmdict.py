from . import app


@app.command()
def jmdict() -> None:
    from pathlib import Path

    from ..jmdict import JMDict

    jmdict = JMDict()
    jmdict.parse(Path.home() / "downloads" / "JMdict.gz")

    print(jmdict.search("話す", "fre")[0].short)
    print("***")
    print(jmdict.search("話す", "fre")[0].extended)
    print("***")
    print(jmdict.search("話す", "eng")[0].short)
    print("***")
    print(jmdict.search("話す", "eng")[0].extended)
