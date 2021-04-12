from typing import List

import torch
import cv2
from common.box import Box
import zope.interface
from tools.Interfaces.bus_detector_interface import IBusDetector


@zope.interface.implementer(IBusDetector)
class BusDetection(object):

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
        self.__results__ = None

    def get_boxes(self) -> List[Box]:
        result_bus = []
        for pred in self.__results__.pred:
            for *box, conf, cls in pred:
                label = f'{self.__results__.names[int(cls)]}'
                if label == "bus":
                    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                    result_bus.append(Box(c1, c2[0], c2[1]))

        return result_bus

    def prediction(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.__results__ = self.model(img, size=640)
