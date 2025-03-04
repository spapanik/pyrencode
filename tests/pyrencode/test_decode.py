import pytest

from pyrencode.decode import Decoder


@pytest.mark.parametrize(
    ("encoded", "error"),
    [
        (b"0", "subsection not found"),
        (b"\x000", "extra data"),
        (b"\xf0", "string of length 0"),
        (b"-1", "unknown type byte"),
        (b"=-0\x7f", "negative zero in int"),
        (b"=01\x7f", "leading zero in int"),
        (
            b"=1000000000000000000000000000000000000000000000000000000000000000\x7f",
            "int exceeds maximum length",
        ),
        (b"01:1", "leading zero in string length"),
    ],
)
def test_value_error(encoded: bytes, error: str) -> None:
    with pytest.raises(ValueError, match=error):
        Decoder.decode(encoded)
