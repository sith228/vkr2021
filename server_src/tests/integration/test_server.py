import socket

import cv2
import pytest
import logging
from typing import List, Mapping

from server.network import Header, Event, Data
from server.network.image_format import ImageFormat
from common.logger import init_logger_test
from tests.checkers.test_checker import Performance
from tests.checkers.test_checker import Accuracy



class TestServer:
    test_data = [Event.BUS_DETECTION, Event.BUS_ROUTE_NUMBER_RECOGNITION]

    @staticmethod
    def func(image, event):
        data = Data.encode_image(image, ImageFormat.JPG_RGB)
        header = Header(event=event, token=0, data_length=len(data)).to_bytes()
        client_socket = socket.socket()
        client_socket.connect(('localhost', 5000))  # TODO: port from constant
        client_socket.send(header + data)
        # Wait for answer
        header = Header(client_socket.recvfrom(Header.LENGTH)[0])

    @pytest.fixture
    def __setup_server(self):
        # server = Server(SimpleNamespace(port=5000, debug=False, output_dir="./debug"))
        # server.run()  # TODO: Run server async

        yield

    @pytest.fixture
    def logger(self):
        init_logger_test()
        return logging.getLogger('test_pipelines')

    def test_session_bus_detection(self, logger):
        image = cv2.imread('test_data/mobilenet_data_v1/2019-10-06 13-12-21.jpg')
        data = Data.encode_image(image, ImageFormat.JPG_RGB)
        header = Header(event=Event.BUS_DETECTION, token=0, data_length=len(data)).to_bytes()
        client_socket = socket.socket()
        client_socket.connect(('localhost', 5000))  # TODO: port from constant
        client_socket.send(header + data)
        # Wait for answer
        header = Header(client_socket.recvfrom(Header.LENGTH)[0])
        n_data = client_socket.recvfrom(header.data_length)[0]
        result = Data.decode_bus_boxes(n_data)
        logger.info('RESULT RESPONSE: ' + str(result))

    def test_session_bus_route_number_recognition(self, logger):
        image = cv2.imread('test_data/mobilenet_data_v1/2019-10-06 13-12-21.jpg')
        data = Data.encode_image(image, ImageFormat.JPG_RGB)
        header = Header(event=Event.BUS_ROUTE_NUMBER_RECOGNITION, token=0, data_length=len(data)).to_bytes()
        client_socket = socket.socket()
        client_socket.connect(('localhost', 5000))  # TODO: port from constant
        client_socket.send(header + data)
        # Wait for answer
        header = Header(client_socket.recvfrom(Header.LENGTH)[0])
        n_data = client_socket.recvfrom(header.data_length)[0]
        result = Data.decode_bus_boxes(n_data)
        logger.info('RESULT RESPONSE: ' + str(result))

    @pytest.mark.parametrize('event', test_data)
    @pytest.mark.skip('CI failed tests with connection error')
    def test_speed_scoring(self, event, logger):
        image = cv2.imread('test_data/mobilenet_data_v1/2019-10-06 13-12-21.jpg')
        test_func = lambda: self.func(image, event)
        logger.info('Performance speed ' + str(event) + ' ' + str(Performance.check(test_func)))

