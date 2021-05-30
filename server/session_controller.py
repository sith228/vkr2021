import socket
from typing import Final
import logging

from server.message.bus_box_message import BusBoxMessage
from server.message.session_message import SessionMessage
from server.session import Session
from server.task import Task
from server.network import Header, Event, Data


class SessionController:
    DEFAULT_DATA_PACKET_LENGTH: Final = 512

    def __init__(self, connection: socket):
        self.logger = logging.getLogger('root')
        self.connection = connection
        self.session = Session()
        self.session.add_callback(self.__session_callback)

    def __listen(self):
        header = Header(self.__receive(Header.LENGTH))
        data = self.__receive(header.data_length)

        if header.event == Event.INIT_SESSION:
            self.__on_init_session(data)
        elif header.event == Event.BUS_DETECTION:
            self.__on_bus_detection(data)
        elif header.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
            self.__on_bus_route_number_recognition(data)

    def __receive(self, length: int):
        result = b''
        remaining_length = length
        while remaining_length > 0:
            result += self.connection.recvfrom(self.DEFAULT_DATA_PACKET_LENGTH
                                               if remaining_length > self.DEFAULT_DATA_PACKET_LENGTH
                                               else remaining_length)[0]
            remaining_length = length - len(result)
        return result

    def __answer(self, header: Header, data: bytes = None):
        try:
            if data is not None:
                self.connection.send(header.to_bytes() + data)
                result = Data.decode_bus_boxes(data)
                self.logger.info('RESULT RESPONSE: ' + str(result))
            else:
                self.connection.send(header.to_bytes())
        except (ConnectionResetError, ConnectionAbortedError):
            return

    # Network event handlers ===========================================================================================
    def __on_init_session(self, data):
        pass

    def __on_bus_detection(self, data):
        image = Data.decode_image(data)
        self.session.push_task(Task(Event.BUS_DETECTION, image))

    def __on_bus_route_number_recognition(self, data):
        image = Data.decode_image(data)
        self.session.push_task(Task(Event.BUS_ROUTE_NUMBER_RECOGNITION, image))

    # Session message handlers =========================================================================================
    def __on_send_bus_box(self, message: BusBoxMessage):
        data = Data.encode_bus_boxes(message.bus_boxes)
        header = Header(event=message.event, token=0, data_length=len(data))  # TODO: Add token
        self.__answer(header, data)

    def __session_callback(self, message: SessionMessage):
        if message.event == Event.BUS_DETECTION or message.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
            self.__on_send_bus_box(message)

    def run(self):
        """
        Starts client listening loop
        :return: none
        """
        try:
            while True:
                self.__listen()
        except (ConnectionResetError, ConnectionAbortedError):
            self.session.close()
            return
