from pipelines.pipeline import Pipeline
from tools.models.bus_detection_yolo.bus_detection import BusDetection

import cv2
import copy
import numpy as np


class BusDetectionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.bus_detector = BusDetection()
        # self.bus_moves_right_detector  # TODO: Add bus moves right detector

    def __is_bus_detected(self) -> dict:
        pass

    def __is_bus_moves_right(self) -> dict:
        pass

    def start_processing(self, data) -> dict:
        """

        :param data: image, number of image
        :return: dict {"boxes": List(Box(bound_box: np.ndarray, width: float, height: float,
                                        probability: float, label='Bus'))}
        """
        image = np.fromstring(data, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.bus_detector.prediction(image)
        return {"boxes": self.bus_detector.get_boxes()}
        pass
