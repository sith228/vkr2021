from __future__ import annotations

import re
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
        self.__check_list__ = {}
        self.height: int = height  # height of box
        self.width: int = width  # width of box
        self.__list_of_inside_boxes__: List[Box] = []  # contain other boxes
        self.__image__: np.ndarray = image.view(image.dtype)

    @staticmethod
    def get_class_of_text(text) -> str:  # ?: What it is
        result = re.match(r"^[0-9]+$", text)  # онли текст
        if result is None:
            result = re.match(r"^[a-z]+$", text)
            if result is None:
                return "num_text"
            else:
                return "text"
        else:
            return "number"

    def get_cropped_image(self):
        points = self.get_bound_box_points()
        return self.__image__[points[2]:points[3], points[0]:points[1]]

    def get_bound_box(self) -> Tuple[int, int, int, int]:
        """
        :return: (x, y, height, width)
        """
        return self.bound_box_coordinates[0], self.bound_box_coordinates[1], self.height, self.width

    def insert_boxes(self, boxes_list: List[Box]):
        for box in boxes_list:
            self.__list_of_inside_boxes__.append(box)

    def get_subboxes(self) -> List[Box]:
        return self.__list_of_inside_boxes__

    def get_bound_box_points(self) -> Tuple[int, int, int, int]:
        """
        :return: (x1, x2, y1, y2)
        """
        return self.bound_box_coordinates[0], self.bound_box_coordinates[0] + self.width, \
               self.bound_box_coordinates[1], self.bound_box_coordinates[1] + self.height

    def update_box(self, box: Box):
        if box.bound_box_coordinates is not None:
            self.bound_box_coordinates = box.bound_box_coordinates
        if box.height is not None:
            self.height = box.height
        if box.width is not None:
            self.width = box.width
        # TODO: update inside boxes
        if box.__image__ is not None:
            self.__image__ = box.__image__

    def set_absolute_coordinates_from_parent(self, parent_box: Box):
        parent_bound_box = parent_box.get_bound_box()
        self.bound_box_coordinates = (self.bound_box_coordinates[0] + parent_bound_box[0],
                                      self.bound_box_coordinates[1] + parent_bound_box[1])

