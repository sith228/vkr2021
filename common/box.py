import re
from typing import List, Any


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
    """

    def __init__(self, bound_box, w, h, angle=0):
        # Add more if can
        self.bound_box_points = bound_box
        self.angle = angle
        self.__check_list__ = {}
        self.text = {}
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

    def insert_box(self, list_boxes):
        """
        Resizes image with keeping aspect ratio
        :param list_boxes: list boxes
        """
        for box in list_boxes:
            self.__list_of_inside_boxes__.append(box)

    def get_subboxes(self) -> List[Any]:
        return self.__list_of_inside_boxes__

    # TODO: Необходимо удалить или изменить
    def get_vino_check(self) -> bool:
        return self.__check_list__["VINO"]

    def get_tesseract_check(self) -> bool:
        return self.__check_list__["TESS"]

    def get_bin_text(self) -> bool:
        return self.__check_list__["BIN"]

    def get_match_check(self) -> bool:
        return self.__check_list__["HAVE_MATCH"]
