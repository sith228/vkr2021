import cv2
import os
import pytest
from types import SimpleNamespace
from urllib.request import Request, urlopen

from common.server import Server
from tests.metrics import Metrics

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
        ip = "http://127.0.0.1"
        port = "5000"
        bus_images_directory = "./test_data/coco_bus/train/"

        images = os.listdir(bus_images_directory)
        image = cv2.imread(bus_images_directory + images[0])
        answer = self.__provide_request(image, ip + ":" + port + "/bus_detection")
        Metrics.write("test_metric", 10)
