from __future__ import annotations

from typing import List, Tuple

import numpy as np


class Box:
    def __init__(self, bound_box_coordinates: Tuple[int, int], height: int, width: int, image: np.ndarray):
        """
        :param bound_box_coordinates: Bound box
        :param height: Height
        :param width: Width
        :param image: OpenCV image
        """
        self.bound_box_coordinates: Tuple[int, int] = bound_box_coordinates
        self.absolute_coordinates: bound_box_coordinates
        self.__check_list__ = {}
        self.height: int = height  # height of box
        self.width: int = width  # width of box
        self.__list_of_inside_boxes__: List[Box] = []  # contain other boxes
        self.__image__: np.ndarray = image.view(image.dtype)

    def get_cropped_image(self) -> np.ndarray:
        """
        Crops image using bound box points values
        :return: np.ndarray
        """
        points = self.get_bound_box_points()
        return self.__image__[points[2]:points[3], points[0]:points[1]]

    def get_bound_box(self) -> Tuple[int, int, int, int]:
        """
        Returns coordinates of bound box on source image
        :return: (x, y, height, width)
        """
        return self.bound_box_coordinates[0], self.bound_box_coordinates[1], self.height, self.width

    def insert_boxes(self, boxes_list: List[Box]):
        """
        Inserts boxes array inside current box
        :param boxes_list: Box that need to be placed inside current box
        :return: none
        """
        for box in boxes_list:
            self.__list_of_inside_boxes__.append(box)

    def get_subboxes(self) -> List[Box]:
        """
        Returns array of inside boxes
        :return: array of inside boxes
        """
        return self.__list_of_inside_boxes__

    def get_bound_box_points(self) -> Tuple[int, int, int, int]:
        """
        Returns coordinates of bound box on source image
        :return: (x1, x2, y1, y2)
        """
        return self.bound_box_coordinates[0], self.bound_box_coordinates[0] + self.width, \
               self.bound_box_coordinates[1], self.bound_box_coordinates[1] + self.height

    def update_box(self, box: Box):
        """
        Updates box with information from given box
        :param box: Box that give information
        :return: none
        """
        if box.bound_box_coordinates is not None:
            self.bound_box_coordinates = box.bound_box_coordinates
        if box.height is not None:
            self.height = box.height
        if box.width is not None:
            self.width = box.width
        # TODO: update inside boxes
        if box.__image__ is not None:
            self.__image__ = box.__image__

    # TODO: cover by tests
    @staticmethod
    def check_intersection(box1: Box, box2: Box) -> bool:
        """
        Checks if first box intersect with second box
        :param box1: First box
        :param box2: Second box
        :return:
        """
        box_a = box1.get_bound_box_points()
        box_b = box2.get_bound_box_points()
        if box_b[0] <= box_a[0] <= box_b[1] or box_a[0] <= box_b[0] <= box_a[1]:
            if box_b[2] <= box_a[2] <= box_b[3] or box_a[2] <= box_b[2] <= box_a[3]:
                return True

        if box_b[0] <= box_a[1] <= box_b[1] or box_a[0] <= box_b[1] <= box_a[1]:
            if box_b[2] <= box_a[3] <= box_b[3] or box_a[2] <= box_b[3] <= box_a[3]:
                return True
        return False

    def set_absolute_coordinates_from_parent(self, parent_box: Box):
        """
        Sets self coordinates with respect to parent image
        :param parent_box: Input parent box
        :return: none
        """
        parent_bound_box = parent_box.get_bound_box()
        self.absolute_coordinates = (self.bound_box_coordinates[0] + parent_bound_box[0],
                                      self.bound_box_coordinates[1] + parent_bound_box[1])

    @staticmethod
    def compare_boxes_area(box1: Box, box2: Box) -> float:
        """
        Compares area of two boxes
        :param box1: First box
        :param box2: Second box
        :return: IoU metric
        """
        box_a = box1.get_bound_box_points()
        box_b = box2.get_bound_box_points()
        x_a = max(box_a[0], box_b[0])
        x_b = min(box_a[1], box_b[1])
        y_a = max(box_a[2], box_b[2])
        y_b = min(box_a[3], box_b[3])

        inter_area = (x_b - x_a + 1) * (y_b - y_a + 1)

        box_a_area = (box_a[1] - box_a[0] + 1) * (box_a[3] - box_a[2] + 1)
        box_b_area = (box_b[1] - box_b[0] + 1) * (box_b[3] - box_b[2] + 1)

        iou = inter_area / float(box_a_area + box_b_area - inter_area)

        return iou
