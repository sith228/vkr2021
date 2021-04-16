from common.box import Box
from typing import Tuple


class TextBox(Box):
    def __init__(self, bound_box: Tuple[int, int], w: int, h: int, text: str = ''):
        super().__init__(bound_box, w, h)
        self.__text__ = text

    def set_text(self, text: str):
        self.__text__ = text

    def get_text(self) -> str:
        return self.__text__
