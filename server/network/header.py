from . import Event


class Header:
    length = 21

    def __init__(self, data: bytes = None, event: Event = None, token: int = None, data_length: int = None):
        if data is not None:
            self.event = Event(int.from_bytes(data[0:1], 'little', signed=False))
            self.token = int.from_bytes(data[1:17], 'little')
            self.data_length = int.from_bytes(data[17:21], 'little')
        else:
            self.event = event
            self.token = token
            self.data_length = data_length

    def to_bytes(self) -> bytes:
        data = b''
        data += self.event.value.to_bytes(1, 'little', signed=False)
        data += self.token.to_bytes(16, 'little')
        data += self.data_length.to_bytes(4, 'little')
        return data
