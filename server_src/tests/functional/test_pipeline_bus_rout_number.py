import cv2
import pytest
import logging

from common.logger import init_logger
from tests.checkers.test_checker import Accuracy
from tools.models.object_detector import ObjectDetectorFactory
from tools.models.text_detector import TextDetectorFactory
from tools.models.text_recognizer import TextRecognizerFactory


class TestBusRoutNumberRecognitionPipeline:
    @pytest.fixture
    def name_data_file(self):
        return './tests/checkers/data_pipeline.txt'

    @pytest.fixture
    def images(self, name_data_file):
        return Accuracy.get_test_image(name_data_file)

    def test_bus_number_recognition(self, name_data_file, images):
        init_logger()
        logger = logging.getLogger('tests')
        bus_detector = ObjectDetectorFactory.get('yolo')
        text_recognizer = TextRecognizerFactory.get('moran')
        text_detector = TextDetectorFactory.get('craft')
        for image_txt in images:
            logger.info('IMAGE: ' + image_txt[0])
            image = cv2.imread(image_txt[0])
            bus_detector.prediction(image)
            bus_boxes = bus_detector.get_boxes()

            for bus_box in bus_boxes:
                logger.info('BOX DETECTED: ' + str(bus_box.get_bound_box()))
                text_detector.prediction(bus_box.get_cropped_image())
                route_number_boxes = text_detector.get_boxes()
                bus_box.insert_boxes(route_number_boxes)

                for route_number_box in route_number_boxes:
                    text_recognizer.prediction(route_number_box.get_cropped_image())
                    route_number_box.text = text_recognizer.get_result()

                Accuracy.check_text_box((image_txt[0], route_number_boxes), name_data_file)
