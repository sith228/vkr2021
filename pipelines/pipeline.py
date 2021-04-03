import logging


@abs
class Pipeline(object):
    def __init__(self):
        self.__debug: bool
        self.__debug_output_dir: str
        self.log = logging.getLogger("root")

    def start_processing(self, data) -> dict:
        raise NotImplementedError
