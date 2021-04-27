from collections import deque
from threading import Semaphore, Thread
from typing import List

import numpy as np

from common.box import BusBox, TextBox
from common.event import Publisher
from server.message.bus_box_message import BusBoxMessage
from server.task import Task
from server.network.event import Event
from pipelines.bus_detection_pipeline import BusDetectionPipeline
from pipelines.bus_door_detection_pipeline import BusDoorDetectionPipeline
from pipelines.bus_route_number_recognition_pipeline import BusRouteNumberRecognitionPipeline


class Session(Publisher):
    def __init__(self):
        super().__init__()

        self.__bus_detection_pipeline = BusDetectionPipeline()

        self.__bus_door_detection_pipeline = BusDoorDetectionPipeline()

        # Setup bus route number recognition pipeline
        self.__bus_route_number_recognition_pipeline = BusRouteNumberRecognitionPipeline()
        self.__bus_route_number_recognition_pipeline.add_handler('update_bus_boxes',
                                                                 self.__interruption_update_bus_boxes)
        self.__bus_route_number_recognition_pipeline.add_handler('update_route_number_boxes',
                                                                 self.__interruption_update_route_number_boxes)
        self.__bus_route_number_recognition_pipeline.add_handler('update_route_number_box_text',
                                                                 self.__interruption_update_route_number_box_text)
        self.__bus_route_number_recognition_pipeline.add_handler('update_bus_route_number',
                                                                 self.__interruption_update_bus_route_number)

        self.__tasks = deque(maxlen=8)  # TODO: Setup deque max len with constant
        self.__tasks_semaphore = Semaphore(0)
        self.__thread = Thread(target=self.run)

        self.__thread.start()

    # Tasks ============================================================================================================
    def __run_bus_detection_pipeline(self, image: np.ndarray):
        result = self.__bus_detection_pipeline.start_processing(image)
        self.__broadcast(BusBoxMessage(Event.BUS_DETECTION, result['boxes']))

    def __run_bus_door_detection_pipeline(self, image: np.ndarray):
        self.__bus_door_detection_pipeline.start_processing(image)

    def __run_bus_route_number_recognition_pipeline(self, image: np.ndarray):
        result = self.__bus_route_number_recognition_pipeline.start_processing(image)
        self.__broadcast(BusBoxMessage(Event.BUS_DETECTION, result['boxes']))

    def run(self):
        while True:
            self.__tasks_semaphore.acquire()
            task = self.__tasks.pop()
            if task.event == Event.BUS_DETECTION:
                self.__run_bus_detection_pipeline(task.image)
            elif task.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
                self.__run_bus_route_number_recognition_pipeline(task.image)
            elif task.event == Event.BUS_DOOR_DETECTION:
                self.__run_bus_route_number_recognition_pipeline(task.image)

    def push_task(self, task: Task):
        self.__tasks.append(task)
        self.__tasks_semaphore.release()

    # Interruptions ====================================================================================================
    def __interruption_update_bus_boxes(self, bus_boxes: List[BusBox]):
        pass

    def __interruption_update_route_number_boxes(self, route_number_boxes: List[TextBox]):
        pass

    def __interruption_update_route_number_box_text(self, route_number_box: TextBox):
        pass

    def __interruption_update_bus_route_number(self, bus_boxes: List[BusBox]):
        pass
