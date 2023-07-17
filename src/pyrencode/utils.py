from __future__ import annotations

from typing import Any


class Singleton(type):
    instance: type[Singleton] | None

    def __init__(cls, name: str, bases: tuple[type, ...], dict_: dict[str, Any]):
        super().__init__(name, bases, dict_)
        cls.instance = None

    def __call__(cls) -> type[Singleton]:
        if cls.instance is None:
            cls.instance = super().__call__()
        return cls.instance


def to_bytes(c: int) -> bytes:  # py310
    return c.to_bytes(length=1, byteorder="big")
