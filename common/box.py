import re
from typing import List, Any, Tuple


# TODO: Расширить класс бокс


class Box(object):
    """

    :param bound_box_points:
    :param angle:
    :param __check_list__:
    :param text:
    :param W: width box
    :param H: height box
    :param list_of_inside_boxes: container other boxes

    :method get_bbox: return Tuple(x, y, width, height) of box
    """

    def __init__(self, bound_box, w, h, angle=0):
        # Add more if can
        self.bound_box_points: Tuple[int, int] = bound_box
        self.angle = angle
        self.__check_list__ = {}
        self.__text__ = ""
        self.height = h  # height of box
        self.width = w  # width of box
        self.__list_of_inside_boxes__ = []  # contain other boxes

    @staticmethod
    def get_class_of_text(text) -> str:
        result = re.match(r"^[0-9]+$", text)  # онли текст
        if result is None:
            result = re.match(r"^[a-z]+$", text)
            if result is None:
                return "num_text"
            else:
                return "text"
        else:
            return "number"

    def get_bbox(self) -> Tuple[int, int, int, int]:
        return self.bound_box_points[0], self.bound_box_points[1], self.width, self.height

    def set_text(self, text: str):
        self.__text__ = text

    def get_text(self) -> str:
        return self.__text__

    def insert_box(self, list_boxes):
        """
        Resizes image with keeping aspect ratio
        :param list_boxes: list boxes
        """
        for box in list_boxes:
            self.__list_of_inside_boxes__.append(box)

    def get_subboxes(self) -> List[Any]:
        return self.__list_of_inside_boxes__