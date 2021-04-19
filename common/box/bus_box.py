from . import Box
from typing import Tuple
import numpy as np


class BusBox(Box):
    def __init__(self, bound_box_coordinates: Tuple[int, int], width: int, height: int, image: np.ndarray):
        super().__init__(bound_box_coordinates, width, height, image)
