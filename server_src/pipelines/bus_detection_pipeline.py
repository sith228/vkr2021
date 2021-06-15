from typing import Dict, List

from common.box import BusBox
from pipelines.pipeline import Pipeline
from tools.models.object_detector import ObjectDetectorFactory
import logging
from datetime import datetime
import cv2
import os

import numpy as np


class BusDetectionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.bus_detector = ObjectDetectorFactory.get('yolo')
        self.logger = logging.getLogger('pipelines')
        global save_results
        # self.bus_moves_right_detector  # TODO: Add bus moves right detector

    def start_processing(self, image: np.ndarray) -> Dict[str, List[BusBox]]:
        """
        Detects buses
        :param image: image
        :return:  Dictionary with list of bus boxes inside
        """
        self.bus_detector.prediction(image)
        self.logger.info('BUS DETECTED: ')
        for bus_detected in self.bus_detector.get_boxes():
            self.logger.info(str(bus_detected.get_bound_box()))
        bus_boxes = self.bus_detector.get_boxes()
        if len(bus_boxes) > 0 and os.environ['save_images'] == 'True':
            name = 'raw_images/' + str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_') + '.jpg'
            cv2.imwrite(name, image)  # TODO: need to delete before release
        return {'boxes': bus_boxes}
