from __future__ import annotations

import struct

import pytest

from pyrencode.decode import loads
from pyrencode.encode import dumps

f1 = struct.unpack("!f", struct.pack("!f", 25.5))[0]
f2 = struct.unpack("!f", struct.pack("!f", 29.3))[0]
f3 = struct.unpack("!f", struct.pack("!f", -0.6))[0]


def test_mixed_types_tuple() -> None:
    obj = (
        (
            {b"a": 15, b"bb": f1, b"ccc": f2, b"": (f3, (), False, True, b"")},
            (b"a", 10**20),
            tuple(range(-100000, 100000)),
            b"b" * 31,
            b"b" * 62,
            b"b" * 64,
            2**30,
            2**33,
            2**62,
            2**64,
            2**30,
            2**33,
            2**62,
            2**64,
            False,
            False,
            True,
            -1,
            2,
            0,
            None,
        ),
    )
    assert loads(dumps(obj)) == obj


def test_tuple_of_updated_dict() -> None:
    d: dict[object, object] = {i: i for i in range(-100000, 100000)}
    d |= {b"a": 20, 20: 40, 40: 41, f1: f2, f2: f3, f3: False, False: True, True: False}
    obj: tuple[object, ...] = (
        d,
        {},
        {5: 6},
        {7: 7, True: 8},
        {9: 10, 22: 39, 49: 50, 44: b""},
    )
    assert loads(dumps(obj)) == obj


def test_tuple_of_bytes() -> None:
    obj = (
        b"",
        b"a" * 10,
        b"a" * 100,
        b"a" * 1000,
        b"a" * 10000,
        b"a" * 100000,
        b"a" * 1000000,
        b"a" * 10000000,
        *tuple(b"a" * n for n in range(1000)),
        b"b",
    )
    assert loads(dumps(obj)) == obj


def test_tuple_of_dicts() -> None:
    obj = (
        tuple(dict(zip(range(n), range(n))) for n in range(100))
        + tuple(dict(zip(range(n), range(-n, 0))) for n in range(100))
        + (b"b",)
    )
    assert loads(dumps(obj)) == obj


def test_tuple_of_tuples() -> None:
    obj = (*tuple(tuple(range(n)) for n in range(100)), b"b")
    assert loads(dumps(obj)) == obj


def test_tuple_of_bool() -> None:
    obj = (None, True, None, False)
    assert loads(dumps(obj)) == obj


def test_none() -> None:
    assert loads(dumps(None)) is None


def test_none_dict() -> None:
    assert loads(dumps({None: None})) == {None: None}


def test_float() -> None:
    assert loads(dumps(1.1)) == pytest.approx(1.1)


def test_float_32() -> None:
    assert loads(dumps(1.1, 32)) == pytest.approx(1.1)


def test_float_64() -> None:
    assert loads(dumps(1.1, 64)) == pytest.approx(1.1)


def test_string() -> None:
    assert loads(dumps("Hello World!!"), decode_utf8=True) == "Hello World!!"
