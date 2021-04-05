import cv2
import pytest
from types import SimpleNamespace
from urllib.request import Request, urlopen

from common.server import Server


class TestServer:

    @pytest.fixture
    def __setup_server(self):
        server = Server(SimpleNamespace(port=5000, debug=False, output_dir="./debug"))
        # server.run()  # TODO: Run server async

        yield

    @staticmethod
    def __provide_request(image, url):
        data = cv2.imencode(".jpg", image)[1].tobytes()
        headers = {"content-type": "image/jpeg"}
        request = Request(url, data=data, headers=headers)
        answer = urlopen(request).read()
        # TODO: Add answer decode
        return answer

    def test_bus_detection(self, __setup_server):
        image = cv2.imread("./test/mobilenet_data_v1/2019-10-06 13-12-21.jpg")
        answer = self.__provide_request(image, "http://127.0.0.1:5000/bus_detection")

