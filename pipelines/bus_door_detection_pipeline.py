from pipelines.pipeline import Pipeline


class BusDoorDetectionPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.door_detector  # TODO: Add detector

    def __is_bus_door_detected(self) -> bool:
        pass

    def __is_bus_door_open(self) -> bool:
        pass

    def start_processing(self, data) -> dict:
        pass
