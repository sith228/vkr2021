import collections

from . import Box
from typing import Tuple, Final
import numpy as np


class TextBox(Box):
    DEQUE_MAXIMUM_LENGTH: Final = 10

    def __init__(self, bound_box_coordinates: Tuple[int, int], height: int, width: int, image: np.ndarray,
                 text: str = ''):
        super().__init__(bound_box_coordinates, height, width, image)
        self.text = text
        self.__text_history__: collections.deque[str] = collections.deque(maxlen=TextBox.DEQUE_MAXIMUM_LENGTH)

    def append_text(self, text: str):
        """
        Appends text to box text history
        :param text: Text to append
        :return: none
        """
        self.__text_history__.append(text)
