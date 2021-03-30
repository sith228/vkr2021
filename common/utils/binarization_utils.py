import cv2
import imutils
import numpy as np


class BinarizationUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def resize_for_open_vino(image):
        # TODO: Add docstring
        image = imutils.resize(image, height=32)
        # image = image_resize(image, height=32)
        if image.shape[1] > 120:
            return cv2.resize(image, (120, 32))

        padd_left = (120 - image.shape[1]) // 2
        padd_right = 120 - padd_left - image.shape[1]

        image = cv2.copyMakeBorder(image, 0, 0, padd_left, padd_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        #cv2.imwrite("{}.jpeg".format(time.time()), image)
        # cv2.imshow("rsize_for_vino", image)
        # cv2.waitKey(1)

        return image

    @staticmethod
    def is_point_in_rect(point, rect):
        # TODO: Add docstring
        if point[0] > rect[0] and point[1] > rect[1]:
            if point[0] < rect[0] + rect[2] and point[1] < rect[1] + rect[3]:
                return True
        return False

    @staticmethod
    def orientate(image):
        # TODO: Add docstring
        bin = image
        # транспонирование изображения
        flipped = cv2.flip(bin, 1)
        (h, w) = flipped.shape[:2]
        center = (w / 2, w / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
        transpose = cv2.warpAffine(flipped, rotation_matrix, (h, w))

        coordinates = np.column_stack(np.where(transpose > 0))
        angle = cv2.minAreaRect(coordinates)[-1]
        if angle < -45:
            angle = -(90 + angle)

        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle
        return angle, BinarizationUtils.rotate_img(image, angle)

    @staticmethod
    def rotate_img(image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (w, h),
                                 borderMode=cv2.BORDER_REPLICATE)
        return rotated
