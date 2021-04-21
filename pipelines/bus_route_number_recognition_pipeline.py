from typing import Dict, Any

import numpy as np
import cv2

from pipelines.pipeline import Pipeline
from tools.models.object_detector import ObjectDetectorFactory
from tools.models.text_detector import TextDetectorFactory
from tools.models.text_recognizer import TextRecognizerFactory


class BusRouteNumberRecognitionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.__bus_detector = ObjectDetectorFactory.get('yolo')
        self.__text_recognizer = TextRecognizerFactory.get('moran')
        self.__text_detector = TextDetectorFactory.get('craft')

    def __is_bus_route_number_detected(self) -> bool:
        pass

    def __is_bus_route_number_recognized(self) -> bool:
        pass

    def start_processing(self, data) -> Dict[str, Any]:
        """
        Detects and recognizes bus route number
        :param data:
        :return: Dictionary with bus
        """
        image = np.fromstring(data, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Bus detection
        self.__bus_detector.prediction(image)
        bus_boxes = self.__bus_detector.get_boxes()
        # TODO: Synchronise boxes with session

        # Route number detection
        for bus_box in bus_boxes:
            self.__text_detector.prediction(bus_box.get_cropped_image())
            route_number_boxes = self.__text_detector.get_boxes()
            bus_box.insert_boxes(route_number_boxes)
            # TODO: Synchronise boxes with session

            # Route number recognition
            for route_number_box in route_number_boxes:
                self.__text_recognizer.prediction(route_number_box.get_cropped_image())
                route_number_box.set_text(self.__text_recognizer.get_result())
                # TODO: Synchronise boxes with session

        return {
            'boxes': bus_boxes,
            'route_number': []  # TODO: Get route number from bus box
        }
