from pipelines.pipeline import Pipeline


class BusRouteNumberDetectionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.text_recognizer  # TODO: Add text recognizer
        self.text_detector  # TODO: Add text detector

    def __is_bus_route_number_detected(self) -> bool:
        pass

    def __is_bus_route_number_recognized(self) -> bool:
        pass

    def start_processing(self, data) -> dict:
        """

        :param data: image, number of image
        :return: dict {"boxes": List(Box(bound_box: np.ndarray, width: float, height: float,
                                        probability: float, text: str))}
        """
        pass

    def add_to_queue(self, data) -> dict:
        # check session
        # detect bus

        pass
