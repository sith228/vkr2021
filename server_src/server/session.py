from collections import deque
from typing import List, Final

import numpy as np
import threading
import time

from common.box import BusBox, TextBox
from common.event import Publisher
from common.utils.box_validator_utils import BoxValidator
from server.message.bus_box_message import BusBoxMessage
from server.task import Task
from server.network.event import Event
from pipelines.bus_detection_pipeline import BusDetectionPipeline
from pipelines.bus_door_detection_pipeline import BusDoorDetectionPipeline
from pipelines.bus_route_number_recognition_pipeline import BusRouteNumberRecognitionPipeline
import logging


class Session(Publisher):
    TASKS_DEQUE_MAXIMUM_LENGTH: Final = 8
    TASK_MAX_TIME_DELAY: Final = 2.0

    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger('root')

        self.__close_flag = False

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

        self.__tasks = deque(maxlen=self.TASKS_DEQUE_MAXIMUM_LENGTH)
        self.__tasks_semaphore = threading.Semaphore(0)
        self.__tasks_mutex = threading.Lock()
        self.__thread = threading.Thread(target=self.__run)
        self.logger.info('Session initialized')

        self.__thread.start()

    # Tasks ============================================================================================================
    def __run_bus_detection_pipeline(self, image: np.ndarray):
        result = self.__bus_detection_pipeline.start_processing(image)
        self.logger.info('RUN BUS DETECTION')
        self.broadcast(BusBoxMessage(Event.BUS_DETECTION, result['boxes']))

    def __run_bus_door_detection_pipeline(self, image: np.ndarray):
        self.logger.info('RUN BUS DOOR DETECTION')
        self.__bus_door_detection_pipeline.start_processing(image)

    def __run_bus_route_number_recognition_pipeline(self, image: np.ndarray):
        self.logger.info('RUN BUS ROUTE NUMBER RECOGNITION')
        result = self.__bus_route_number_recognition_pipeline.start_processing(image)
        self.broadcast(BusBoxMessage(Event.BUS_DETECTION, result['boxes']))

    def __run(self):
        """
        Starts session
        :return: none
        """
        while True:
            if self.__close_flag:
                return
            self.__remove_old_tasks()
            self.__tasks_semaphore.acquire()
            try:
                task = self.__tasks.pop()
            except IndexError:  # TODO: Remove this if never happens
                self.logger.error('Session synchronisation error')
                continue
            if task.event == Event.BUS_DETECTION:
                self.__run_bus_detection_pipeline(task.image)
            elif task.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
                self.__run_bus_route_number_recognition_pipeline(task.image)
            elif task.event == Event.BUS_DOOR_DETECTION:
                self.__run_bus_route_number_recognition_pipeline(task.image)

    def __remove_old_tasks(self):
        self.__tasks_mutex.acquire()
        while self.__tasks and time.time() - self.__tasks[0].creation_time > self.TASK_MAX_TIME_DELAY:
            self.__tasks_semaphore.acquire()
            self.__tasks.popleft()
        self.__tasks_mutex.release()

    def push_task(self, task: Task):
        """
        Pushes task in queue
        :param task: Task to do
        :return: none
        """
        self.logger.info('Push task -> ' + str(task.event))
        self.__tasks_mutex.acquire()
        is_need_to_semaphore_release = False
        if len(self.__tasks) < 8:
            is_need_to_semaphore_release = True
        self.__tasks.append(task)
        if is_need_to_semaphore_release:
            self.__tasks_semaphore.release()
        self.__tasks_mutex.release()

    def close(self):
        self.__close_flag = True

    # Interruptions ====================================================================================================
    def __interruption_update_bus_boxes(self, bus_boxes: List[BusBox]):
        pass

    def __interruption_update_route_number_boxes(self, route_number_boxes: List[TextBox]):
        pass

    def __interruption_update_route_number_box_text(self, route_number_box: TextBox):
        pass

    def __interruption_update_bus_route_number(self, bus_boxes: List[BusBox]):
        for bus_box in bus_boxes:
            for text_box in bus_box.get_subboxes():
                if BoxValidator.has_valid_text(text_box):
                    bus_box.route_number = text_box.text
                    self.logger.info('BUS ROUT = ' + bus_box.route_number)
                    break
