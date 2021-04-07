from tools.models.bus_detection_yolo.bus_detection import BusDetection
import cv2
import pytest


class TestBusDetection:
    @pytest.mark.skip
    def test_bus_detection(self):
        bus_detector = BusDetection()
        image = cv2.imread('./test_data/text_sample.png')
        bus_detector.prediction(image)
        assert len(bus_detector.result()) != 0
