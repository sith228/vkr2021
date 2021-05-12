from tools.models.object_detectors.yolo.bus_detection import BusDetection
from tests.checkers.test_checker import Accuracy
import cv2
import pytest


class TestBusDetection:
    @pytest.fixture
    def images(self):
        return Accuracy.get_test_image('./tests/checkers/data.txt')

    def test_bus_detection(self, images):
        bus_detector = BusDetection()
        # images = Accuracy.get_test_image('./tests/checkers/data.txt')
        list_for_check = []
        for test_image in images:
            image = cv2.imread(test_image[0])
            bus_detector.prediction(image)
            list_for_check.append((test_image[0], bus_detector.get_boxes()[0]))
        Accuracy.check_boxes(list_for_check)
