from common.event import Message
from server.network.event import Event


class SessionMessage(Message):
    def __init__(self, event: Event):
        self.event = event
