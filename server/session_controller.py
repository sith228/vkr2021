import socket

from common.session import Session
from server.network import Header, Event


class SessionController:
    def __init__(self, connection: socket):
        self.connection = connection
        self.session = Session()

    def __listen(self):
        header = Header(self.connection.recvfrom(Header.length)[0])
        data = b''
        while len(data) < header.data_length:
            data += self.connection.recvfrom(512)[0]  # TODO: Setup packet size from constant

        if header.event == Event.INIT_SESSION:
            self.__on_init_session(data)
        elif header.event == Event.BUS_DOOR_DETECTION:
            self.__on_bus_door_detection(data)

    def __on_init_session(self, data):
        pass

    def __on_bus_door_detection(self, data):
        pass

    def run(self):
        while True:
            self.__listen()
