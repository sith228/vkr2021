import collections

from . import Box
from typing import Tuple
import numpy as np


class TextBox(Box):
    def __init__(self, bound_box_coordinates: Tuple[int, int], height: int, width: int, image: np.ndarray,
                 text: str = ''):
        super().__init__(bound_box_coordinates, height, width, image)
        self.__text__ = text
        self.__text_history__: collections.deque[str] = collections.deque(maxlen=10)  # TODO: maxlen move to constant

    def set_text(self, text: str):
        self.__text__ = text

    def get_text(self) -> str:
        return self.__text__

    def append_text(self, text: str):
        self.__text_history__.append(text)
