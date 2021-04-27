import socket
from typing import List

from common.box import BusBox
from server.message.bus_box_message import BusBoxMessage
from server.message.session_message import SessionMessage
from server.session import Session
from server.task import Task
from server.network import Header, Event, Data


class SessionController:
    def __init__(self, connection: socket):
        self.connection = connection
        self.session = Session()
        self.session.add_callback(self.__session_callback)

    def __listen(self):
        header = Header(self.connection.recvfrom(Header.length)[0])
        data = b''
        while len(data) < header.data_length:
            data += self.connection.recvfrom(512)[0]  # TODO: Setup packet size from constant

        if header.event == Event.INIT_SESSION:
            self.__on_init_session(data)
        elif header.event == Event.BUS_DETECTION:
            self.__on_bus_detection(data)

    def __answer(self, header: Header, data: bytes = None):
        if data is not None:
            self.connection.send(header.to_bytes() + data)
        else:
            self.connection.send(header.to_bytes())

    # Network event handlers ===========================================================================================
    def __on_init_session(self, data):
        pass

    def __on_bus_detection(self, data):
        image = Data.decode_image(data)
        self.session.push_task(Task(Event.BUS_DETECTION, image))

    # Session message handlers =========================================================================================
    def __on_send_bus_box(self, message: BusBoxMessage):
        data = Data.encode_bus_boxes(message.bus_boxes)
        header = Header(event=message.event, token=0, data_length=len(data))  # TODO: Add token
        self.__answer(header, data)

    def __session_callback(self, message: SessionMessage):
        if message.event == Event.BUS_DETECTION or message.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
            self.__on_send_bus_box(message)

    def run(self):
        try:
            while True:
                self.__listen()
        except ConnectionResetError:
            return
