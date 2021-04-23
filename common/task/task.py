import numpy as np

from . import Mode


class Task:
    def __init__(self, mode: Mode, image: np.ndarray = None):
        self.mode = mode
        self.image = image
