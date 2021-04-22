import logging
import numpy as np

from common.event import Interruptible


class Pipeline(Interruptible):
    def __init__(self):
        super().__init__()
        self.__debug: bool
        self.__debug_output_dir: str
        self.log = logging.getLogger("root")

    def start_processing(self, image: np.ndarray) -> dict:
        raise NotImplementedError
