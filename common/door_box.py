from common.box import Box
from typing import Tuple
import numpy as np


class DoorBox(Box):
    def __init__(self, bound_box: Tuple[int, int], w: int, h: int, image: np.ndarray):
        super().__init__(bound_box, w, h, image.view())
