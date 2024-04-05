from . import app


@app.command()
def jmdict() -> None:
    from ..jmdict import load as jmdict_load

    jmdict = jmdict_load()

    print(jmdict.search("話す", "fre")[0].short)
    print("***")
    print(jmdict.search("話す", "fre")[0].extended)
    print("***")
    print(jmdict.search("話す", "eng")[0].short)
    print("***")
    print(jmdict.search("話す", "eng")[0].extended)
