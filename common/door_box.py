from common.box import Box
from typing import Tuple


class DoorBox(Box):
    def __init__(self, bound_box: Tuple[int, int], w: int, h: int):
        super().__init__(bound_box, w, h)
