import json
import urllib.request
from typing import Any
from urllib.error import URLError

from .utils import Stats, error


class AnkiConnect:
    @classmethod
    def find_notes(cls, query: str) -> list[int]:
        return cls._invoke("findNotes", query=query)

    @classmethod
    def notes_info(cls, note_ids: list[int]) -> list[dict[str, Any]]:
        return cls._invoke("notesInfo", notes=note_ids)

    @classmethod
    def update_note_fields(cls, id: int, fields: dict[str, str]) -> None:
        cls._invoke("updateNoteFields", note=dict(id=id, fields=fields))

    @classmethod
    def update_field_with_stats(
        cls,
        note_info: dict[str, Any],
        field: str,
        new_value: str,
        stats: Stats,
    ) -> None:
        old_value = note_info["fields"][field]["value"]
        if new_value != old_value:
            if not old_value:
                stats.added += 1
            else:
                stats.modified += 1
            cls.update_note_fields(note_info["noteId"], {field: new_value})

    @classmethod
    def add_note(cls, deck_name: str, model_name: str, fields: dict[str, str]) -> None:
        result = cls._invoke(
            "addNote",
            note=dict(
                deckName=deck_name,
                modelName=model_name,
                fields=fields,
                options=dict(
                    allowDuplicate=False,
                    duplicateScope="deck",
                    duplicateScopeOptions=dict(
                        deckName=deck_name, checkAllModels=False
                    ),
                ),
            ),
        )
        if not result:
            raise Exception(f"Could not create card with fields {fields}.")

    @staticmethod
    def _invoke(action: str, **params: Any) -> Any:
        request_json = json.dumps(dict(action=action, params=params, version=6)).encode(
            "utf-8"
        )
        try:
            response = json.load(
                urllib.request.urlopen(
                    urllib.request.Request("http://localhost:8765", request_json)
                )
            )
        except URLError:
            error("Could not open Anki Connect URL. Is Anki running?")
        if len(response) != 2:
            error("Response has an unexpected number of fields")
        if "error" not in response:
            error("Response is missing required error field")
        if "result" not in response:
            error("Response is missing required result field")
        if response["error"] is not None:
            error(response["error"])
        return response["result"]
