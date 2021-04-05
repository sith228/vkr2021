from pipelines.pipeline import Pipeline


class BusDetectionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        # self.bus_detector  # TODO: Add bus detector
        # self.bus_moves_right_detector  # TODO: Add bus moves right detector

    def __is_bus_detected(self) -> dict:
        pass

    def __is_bus_moves_right(self) -> dict:
        pass

    def start_processing(self, data) -> dict:
        """

        :param data: image, number of image
        :return: dict {"boxes": List(Box(bound_box: np.ndarray, width: float, height: float,
                                        probability: float, label='Bus'))}
        """
        pass
