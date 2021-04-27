from typing import List

from common.box import BusBox
from server.message.session_message import SessionMessage
from server.network import Event


class BusBoxMessage(SessionMessage):
    def __init__(self, event: Event, bus_boxes: List[BusBox]):
        super().__init__(event)
        self.bus_boxes = bus_boxes
