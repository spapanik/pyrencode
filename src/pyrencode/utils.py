def to_bytes(c: int) -> bytes:  # TODO (py3.10): these are now the default values
    return c.to_bytes(length=1, byteorder="big")
