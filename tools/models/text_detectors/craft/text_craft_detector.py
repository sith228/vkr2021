from typing import List

from craft_text_detector import Craft, get_prediction
import cv2

from common.box import Box
from tools.Interfaces.text_detector_interface import ITextDetector


class CraftDetection(ITextDetector):
    def __init__(self, cuda: bool):
        self.__model__ = Craft(crop_type="box", cuda=cuda, refiner=False, rectify=False)
        self.__results__ = None
        self.__image__ = None

    def prediction(self, image):
        self.__image__ = image.view()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if image.shape[0] == 2:
            image = image[0]
        if image.shape[2] == 4:
            image = image[:, :, :3]

        self.__results__ = get_prediction(
            image=image,
            craft_net=self.__model__.craft_net,
            text_threshold=self.__model__.text_threshold,
            link_threshold=self.__model__.link_threshold,
            low_text=self.__model__.low_text,
            cuda=self.__model__.cuda,
            long_size=self.__model__.long_size,
        )

    def get_boxes(self) -> List[Box]:
        result_text_box = []
        for box in self.__results__['boxes']:
            result_text_box.append(TextBox((box[0][0], box[0][1]), box[2][0] - box[0][0], box[2][1] - box[0][1], self.__image__))

        return result_text_box
