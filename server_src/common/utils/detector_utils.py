import cv2
import numpy as np
from typing import Any, Tuple


class DetectorUtils(object):
    @staticmethod
    def min_area_rect(contour: np.ndarray) -> Tuple[Any, int, int, int]:
        """
        Returns minAreaRect of contour
        :param contour: Contour
        :return: Outline angled rectangle
        """
        rect = cv2.minAreaRect(contour)
        width, height = rect[1]
        angle = rect[-1]
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        return box, width, height, angle

    @staticmethod
    def get_bound_box(contour: np.ndarray) -> Tuple[np.ndarray, int, int]:
        """
        :param contour: Contour
        :return: Outline rectangle
        """
        x, y, width, height = cv2.boundingRect(contour)
        return np.asarray([[x, y], [x + width, y + height]]), width, height

    @staticmethod
    def order_points(rectangle) -> np.ndarray:
        """
        Order: TL, TR, BR, BL
        :param rectangle: Rectangle
        :return: Rectangle with ordered point
        """
        result = np.zeros_like(rectangle)
        sums = rectangle.sum(axis=1)
        result[0] = rectangle[np.argmin(sums)]
        result[2] = rectangle[np.argmax(sums)]
        diff = np.diff(rectangle, axis=1)
        result[1] = rectangle[np.argmin(diff)]
        result[3] = rectangle[np.argmax(diff)]
        return result
