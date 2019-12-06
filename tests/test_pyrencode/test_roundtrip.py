import struct

from pyrencode.decode import loads
from pyrencode.encode import dumps

f1 = struct.unpack("!f", struct.pack("!f", 25.5))[0]
f2 = struct.unpack("!f", struct.pack("!f", 29.3))[0]
f3 = struct.unpack("!f", struct.pack("!f", -0.6))[0]


def test_mixed_types_tuple():
    obj = (
        (
            {b"a": 15, b"bb": f1, b"ccc": f2, b"": (f3, (), False, True, b"")},
            (b"a", 10 ** 20),
            tuple(range(-100000, 100000)),
            b"b" * 31,
            b"b" * 62,
            b"b" * 64,
            2 ** 30,
            2 ** 33,
            2 ** 62,
            2 ** 64,
            2 ** 30,
            2 ** 33,
            2 ** 62,
            2 ** 64,
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


def test_tuple_of_updated_dict():
    d = dict(zip(range(-100000, 100000), range(-100000, 100000)))
    d.update(
        {b"a": 20, 20: 40, 40: 41, f1: f2, f2: f3, f3: False, False: True, True: False}
    )
    obj = (d, {}, {5: 6}, {7: 7, True: 8}, {9: 10, 22: 39, 49: 50, 44: b""})
    assert loads(dumps(obj)) == obj


def test_tuple_of_bytes():
    obj = (
        (
            b"",
            b"a" * 10,
            b"a" * 100,
            b"a" * 1000,
            b"a" * 10000,
            b"a" * 100000,
            b"a" * 1000000,
            b"a" * 10000000,
        )
        + tuple(b"a" * n for n in range(1000))
        + (b"b",)
    )
    assert loads(dumps(obj)) == obj


def test_tuple_of_dicts():
    obj = (
        tuple(dict(zip(range(n), range(n))) for n in range(100))
        + tuple(dict(zip(range(n), range(-n, 0))) for n in range(100))
        + (b"b",)
    )
    assert loads(dumps(obj)) == obj


def test_tuple_of_tuples():
    obj = tuple(tuple(range(n)) for n in range(100)) + (b"b",)
    assert loads(dumps(obj)) == obj


def test_tuple_of_bool():
    obj = (None, True, None, False)
    assert loads(dumps(obj)) == obj


def test_none():
    assert loads(dumps(None)) is None


def test_none_dict():
    assert loads(dumps({None: None})) == {None: None}


def test_float():
    assert 1e-10 < abs(loads(dumps(1.1)) - 1.1) < 1e-6


def test_float_32():
    assert 1e-10 < abs(loads(dumps(1.1, 32)) - 1.1) < 1e-6


def test_float_64():
    assert abs(loads(dumps(1.1, 64)) - 1.1) < 1e-12


def test_string():
    assert loads(dumps("Hello World!!"), decode_utf8=True) == "Hello World!!"
