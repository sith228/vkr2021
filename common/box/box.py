from __future__ import annotations

import re
from typing import List, Tuple

import numpy as np


class Box:
    def __init__(self, bound_box_coordinates, width, height, image: np.ndarray):
        """
        :param bound_box_coordinates: Bound box
        :param width: Width
        :param height: Height
        :param image: OpenCV image
        """
        self.bound_box_coordinates: Tuple[int, int] = bound_box_coordinates
        self.__check_list__ = {}
        self.height = height  # height of box
        self.width = width  # width of box
        self.__list_of_inside_boxes__ = []  # contain other boxes
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
        return self.__image__[points[0]:points[1], points[2]:points[3]]

    def get_bound_box(self) -> Tuple[int, int, int, int]:
        """
        :return: (x, y, width, height)
        """
        return self.bound_box_coordinates[0], self.bound_box_coordinates[1], self.width, self.height

    def insert_boxes(self, boxes_list):
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
