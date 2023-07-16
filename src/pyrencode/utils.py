def to_bytes(c: int) -> bytes:  # py310
    return c.to_bytes(length=1, byteorder="big")
