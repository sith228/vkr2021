import numpy as np

from pipelines.pipeline import Pipeline


class BusDoorDetectionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        # self.door_detector  # TODO: Add detector

    def start_processing(self, image: np.ndarray) -> dict:
        """
        Detects bus doors
        :param image: image
        :return:
        """
        pass
