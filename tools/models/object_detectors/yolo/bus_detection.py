from typing import List

import torch
import cv2
import numpy as np
from common.bus_box import Box, BusBox
from tools.Interfaces.bus_detector_interface import IBusDetector


class BusDetection(IBusDetector):

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
        self.__results__ = None
        self.__image__ = None

    def get_boxes(self) -> List[Box]:
        result_bus = []
        for pred in self.__results__.pred:
            for *box, conf, cls in pred:
                label = f'{self.__results__.names[int(cls)]}'
                if label == "bus":
                    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                    result_bus.append(BusBox(c1, c2[0], c2[1], self.__image__))

        return result_bus

    def prediction(self, img: np.ndarray):
        self.__image__ = img.view()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.__results__ = self.model(img, size=640)
