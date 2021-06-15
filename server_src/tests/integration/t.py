import socket
import cv2

from server.network import Data, Header, Event
from server.network.image_format import ImageFormat


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