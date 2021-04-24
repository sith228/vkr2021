from . import Event


class Header:
    length = 21

    def __init__(self, data: bytes):
        self.event = Event(int.from_bytes(data[0:1], 'little'))
        self.token = int.from_bytes(data[1:17], 'little')
        self.data_length = int.from_bytes(data[17:21], 'little')

    def to_bytes(self) -> bytes:
        data = b''
        data += self.event.value.to_bytes(1, 'little')
        data += self.token.to_bytes(16, 'little')
        data += self.data_length.to_bytes(4, 'little')
        return data
