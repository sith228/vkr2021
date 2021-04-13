import logging

from common.event.interruptible import Interruptible


class Pipeline(Interruptible):
    def __init__(self):
        super().__init__()
        self.__debug: bool
        self.__debug_output_dir: str
        self.log = logging.getLogger("root")

    def start_processing(self, data) -> dict:
        raise NotImplementedError
