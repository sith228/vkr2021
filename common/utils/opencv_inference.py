import cv2
import numpy as np


class OpenCvInference(object):
    def __init__(self, xml_path: str, bin_path: str, width: int, height: int):
        self.__td_net = cv2.dnn.readNet(xml_path, bin_path)
        self.__height = height
        self.__width = width

    def inference_sync(self, frame: np.ndarray):
        # TODO: add docstring
        blob = cv2.dnn.blobFromImage(frame, 1, (self.__height, self.__width), ddepth=cv2.CV_8U)
        self.__td_net.setInput(blob)
        out = self.__td_net.forward(self.__td_net.getUnconnectedOutLayersNames())
        return out
