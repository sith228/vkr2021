from typing import Dict

from common.box import BusBox
from pipelines.pipeline import Pipeline
from tools.models.object_detector import ObjectDetectorFactory

import cv2
import numpy as np


class BusDetectionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.bus_detector = ObjectDetectorFactory.get('yolo')
        # self.bus_moves_right_detector  # TODO: Add bus moves right detector

    def __is_bus_detected(self) -> dict:
        pass

    def __is_bus_moves_right(self) -> dict:
        pass

    def start_processing(self, data) -> Dict[str, BusBox]:
        """
        Detects buses
        :param data:
        :return:  Dictionary with list of bus boxes inside
        """
        image = np.fromstring(data, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.bus_detector.prediction(image)
        return {'boxes': self.bus_detector.get_boxes()}
