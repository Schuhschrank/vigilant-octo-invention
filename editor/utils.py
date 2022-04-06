from typing import Any


def populate_obj(obj: object, data: dict[str, Any]):
    for key, value in data.items():
        obj.__setattr__(key, value)
