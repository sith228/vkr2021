import socket

from server.session import Session
from common.task import Task, Mode
from server.network import Header, Event, Data


class SessionController:
    def __init__(self, connection: socket):
        self.connection = connection
        self.session = Session()
        self.session.add_callback(self.__session_callback)
        self.session.run()

    def __listen(self):
        header = Header(self.connection.recvfrom(Header.length)[0])
        data = b''
        while len(data) < header.data_length:
            data += self.connection.recvfrom(512)[0]  # TODO: Setup packet size from constant

        if header.event == Event.INIT_SESSION:
            self.__on_init_session(data)
        elif header.event == Event.BUS_DOOR_DETECTION:
            self.__on_bus_door_detection(data)

    def __answer(self, header: Header, data=None):
        self.connection.send(header.to_bytes())
        # TODO: send data

    # Network event handlers ===========================================================================================
    def __on_init_session(self, data):
        pass

    def __on_bus_door_detection(self, data):
        image = Data.decode_image(data)
        self.session.push_task(Task(Mode.BUS_DOOR_DETECTION, image))

    def __session_callback(self, message):
        pass

    def run(self):
        while True:
            self.__listen()
