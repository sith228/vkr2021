from typing import Dict, List

from common.box import BusBox
from pipelines.pipeline import Pipeline
from tools.models.object_detector import ObjectDetectorFactory

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

    def start_processing(self, image: np.ndarray) -> Dict[str, List[BusBox]]:
        """
        Detects buses
        :param image:
        :return:  Dictionary with list of bus boxes inside
        """
        self.bus_detector.prediction(image)
        return {'boxes': self.bus_detector.get_boxes()}
