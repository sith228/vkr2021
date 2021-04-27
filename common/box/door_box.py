from . import Box
from typing import Tuple
import numpy as np


class DoorBox(Box):
    def __init__(self, bound_box_coordinates: Tuple[int, int], height: int, width: int, image: np.ndarray):
        super().__init__(bound_box_coordinates, height, width, image)
