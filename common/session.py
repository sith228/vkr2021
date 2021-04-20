from collections import deque
from typing import List

from common.box import Box
from common.event import Publisher
from pipelines.bus_detection_pipeline import BusDetectionPipeline
from pipelines.bus_door_detection_pipeline import BusDoorDetectionPipeline
from pipelines.bus_route_number_recognition_pipeline import BusRouteNumberRecognitionPipeline


class Session(Publisher):
    def __init__(self, bus_detection_pipeline: BusDetectionPipeline,
                 route_detection_pipeline: BusRouteNumberRecognitionPipeline,
                 door_detection_pipeline: BusDoorDetectionPipeline):
        super().__init__()
        self.__status = {'bus_detected': False,
                         'route_number_detected': False,
                         'route_number_recognized': False,
                         'door_detected': False}
        self.__images_to_process = deque()
        self.__bus_detection_pipeline = bus_detection_pipeline
        self.__route_detection_pipeline = route_detection_pipeline
        self.__door_detection_pipeline = door_detection_pipeline
        self.__updated = False
        #                             # dict {"boxes": List(Box(bound_box: np.ndarray, width: float, height: float,
        #                             # probability: float, label='Bus'))}
        '''
        LIMITATION - only one bus arrived at bus stop
        So max length if __boxes_array == 1
        '''
        self.__boxes_array: List[Box] = []  # Store boxes of buses

    def append_image(self, image):
        self.__images_to_process.append(image)

    def run_pipelines(self):
        image_to_process = self.__images_to_process.pop()
        if self.__status['bus_detected']:
            if not self.__status['route_number_detected']:
                self.__route_detection_pipeline.start_processing(image_to_process)
                if not self.__status['route_number_recognized']:
                    self.__route_detection_pipeline.start_processing(image_to_process)
            else:
                self.__door_detection_pipeline.start_processing(image_to_process)
        else:
            self.__bus_detection_pipeline.start_processing(image_to_process)

    def on_result(self, message):
        self.__updated = True
        # send answer to phone self.server.return_result(id, message)
        # TODO Run in new thread
        self.broadcast(message)

    def get_result(self):
        if self.__updated:
            # TODO return last state
            return self.__status
        else:
            return False
