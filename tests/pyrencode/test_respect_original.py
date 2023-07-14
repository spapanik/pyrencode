import struct

import pytest
from rencode import dumps as dumps_orig, loads as loads_orig

from pyrencode import dumps, loads

f1 = struct.unpack("!f", struct.pack("!f", 25.5))[0]
f2 = struct.unpack("!f", struct.pack("!f", 29.3))[0]
f3 = struct.unpack("!f", struct.pack("!f", -0.6))[0]


@pytest.mark.parametrize(
    "obj",
    [
        {b"a": 15, b"bb": f1, b"ccc": f2, b"": (f3, (), False, True, b"")},
        (b"a", 10**20),
        list(range(-100000, 100000)),
        b"b" * 31,
        b"b" * 64,
        2**64,
        2**30,
        2**33,
        2**62,
        2**64,
        -1,
        2,
        0,
        None,
        {None: None},
        False,
        True,
        1.01,
        "a string",
        [1, 2, 3, True],
    ],
)
def test_dump_and_load(obj):
    original = dumps_orig(obj)
    assert dumps(obj) == original
    assert loads(original) == loads_orig(original)


def test_dump_and_load_with_decode():
    original = dumps_orig("Hello World!")
    assert loads(original, decode_utf8=True) == loads_orig(original, decode_utf8=True)
