import socket

import cv2
import pytest

from server.network import Header, Event, Data
from server.network.image_format import ImageFormat


class TestServer:
    @pytest.fixture
    def __setup_server(self):
        # server = Server(SimpleNamespace(port=5000, debug=False, output_dir="./debug"))
        # server.run()  # TODO: Run server async

        yield

    def test_session_bus_detection(self):
        image = cv2.imread('test_data/mobilenet_data_v1/2019-10-06 13-12-21.jpg')
        data = Data.encode_image(image, ImageFormat.RAW_BGR)
        header = Header(event=Event.BUS_DETECTION, token=0, data_length=len(data)).to_bytes()
        client_socket = socket.socket()
        client_socket.connect(('localhost', 5000))  # TODO: port from constant
        client_socket.send(header + data)
        # Wait for answer
        header = Header(client_socket.recvfrom(Header.length)[0])
