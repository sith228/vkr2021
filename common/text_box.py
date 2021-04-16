from common.box import Box
from typing import Tuple, List
import numpy as np


class TextBox(Box):
    def __init__(self, bound_box: Tuple[int, int], w: int, h: int, image: np.ndarray, text: str = ''):
        super().__init__(bound_box, w, h, image)
        self.__text__ = text
        self.__text_container__: List[str] = []

    def set_text(self, text: str):
        self.__text__ = text

    def get_text(self) -> str:
        return self.__text__

    def append_text(self, text: str):
        self.__text_container__.append(text)
        if len(self.__text_container__) > 10:
            del self.__text_container__[0]
