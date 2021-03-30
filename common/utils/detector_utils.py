import cv2
import numpy as np


class DetectorUtils(object):
    @staticmethod
    def min_area_rect(cnt):
        # TODO: Add docstring
        rect = cv2.minAreaRect(cnt)
        w, h = rect[1]
        angle = rect[-1]
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        return box, w, h, angle

    @staticmethod
    def get_bound_box(cnt):
        # TODO: ADD docstring
        x, y, w, h = cv2.boundingRect(cnt)
        return np.asarray([[x, y], [x + w, y + h]]), w, h

    @staticmethod
    def order_points(rect):
        # TODO: ADD docstring
        """ (x, y)
            Order: TL, TR, BR, BL
        """
        tmp = np.zeros_like(rect)
        sums = rect.sum(axis=1)
        tmp[0] = rect[np.argmin(sums)]
        tmp[2] = rect[np.argmax(sums)]
        diff = np.diff(rect, axis=1)
        tmp[1] = rect[np.argmin(diff)]
        tmp[3] = rect[np.argmax(diff)]
        return tmp
