from collections import deque

from common.event.publisher import Publisher
from pipelines.bus_detection_pipeline import BusDetectionPipeline
from pipelines.bus_door_detection_pipeline import BusDoorDetectionPipeline
from pipelines.bus_route_number_detection_pipeline import BusRouteNumberDetectionPipeline


class Session(Publisher):
    def __init__(self, bus_detection_pipeline: BusDetectionPipeline,
                 route_detection_pipeline: BusRouteNumberDetectionPipeline,
                 door_detection_pipeline: BusDoorDetectionPipeline):
        super().__init__()
        self.status = {'bus_detected': False,
                       'route_number_detected': False,
                       'route_number_recognized': False,
                       'door_detected': False}
        self.deque = deque()
        self.bus_detection_pipeline = bus_detection_pipeline
        self.route_detection_pipeline = route_detection_pipeline
        self.door_detection_pipeline = door_detection_pipeline
        self.updated = False

    def append_image(self, image):
        self.deque.append(image)

    def run_pipelines(self):
        image_to_process = self.deque.pop()
        if self.status['bus_detected']:
            if not self.status['route_number_detected']:
                self.route_detection_pipeline.start_processing(image_to_process)
                if not self.status['route_number_recognized']:
                    self.route_detection_pipeline.start_processing(image_to_process)
            else:
                self.door_detection_pipeline.start_processing(image_to_process)
        else:
            self.bus_detection_pipeline.start_processing(image_to_process)

    def on_result(self, message):
        self.updated = True
        # send answer to phone self.server.return_result(id, message)
        # TODO Run in new thread
        self.broadcast(message)

    def get_result(self):
        if self.updated:
            # TODO return last state
            return self.status
        else:
            return False
