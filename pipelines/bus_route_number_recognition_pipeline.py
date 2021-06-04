from typing import Dict, List
from datetime import datetime

import numpy as np
import cv2

from common.box import BusBox
from common.utils.box_validator_utils import BoxValidator
from pipelines.pipeline import Pipeline
from server.message.bus_box_message import BusBoxMessage
from tools.models.object_detector import ObjectDetectorFactory
from tools.models.text_detector import TextDetectorFactory
from tools.models.text_recognizer import TextRecognizerFactory
from common.logger import Logger
import logging


class BusRouteNumberRecognitionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        logging.setLoggerClass(Logger)
        self.logger = logging.getLogger("pipelines")
        self.__bus_detector = ObjectDetectorFactory.get('yolo')
        self.__text_recognizer = TextRecognizerFactory.get('moran')
        self.__text_detector = TextDetectorFactory.get('craft')
        self.logger.info('Pipeline initialized')

    def start_processing(self, image: np.ndarray) -> Dict[str, List[BusBox]]:
        """
        Detects and recognizes bus route number
        :param image: image
        :return: Dictionary with bus
        """
        # Bus detection
        self.__bus_detector.prediction(image)
        bus_boxes = self.__bus_detector.get_boxes()
        # TODO: Synchronise boxes with session

        # Route number detection
        for bus_box in bus_boxes:
            self.__text_detector.prediction(bus_box.get_cropped_image())
            self.logger.info('BUS BOX: ' + str(bus_box.get_bound_box()))
            route_number_boxes = self.__text_detector.get_boxes()
            bus_box.insert_boxes(route_number_boxes)
            # TODO: Synchronise boxes with session

            # Route number recognition
            for route_number_box in route_number_boxes:
                route_number_box.set_absolute_coordinates_from_parent(bus_box)
                self.__text_recognizer.prediction(route_number_box.get_cropped_image())

                route_number_box.text = self.__text_recognizer.get_result()
                self.logger.info('ROUT BOX: ' + str(route_number_box.get_bound_box()))
                self.logger.info('ROUT NUMBER: ' + route_number_box.text)
                if BoxValidator.has_valid_text(route_number_box):
                    name = 'cropped_moran/' + str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ',
                                                                                                              '_') + '.jpg'
                    cv2.imwrite(name, route_number_box.get_cropped_image())  # TODO: need to delete before release
                # TODO: Synchronise boxes with session
        self.interrupt('update_bus_route_number', bus_boxes)
        if len(bus_boxes) > 0:
            name = 'raw_images/' + str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_') + '.jpg'
            cv2.imwrite(name, image)  # TODO: need to delete before release
        return {
            'boxes': bus_boxes,
        }
