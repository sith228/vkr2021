from abc import ABC

import tools.models.object_detectors.yolo.bus_detection


class ObjectDetectorFactory(ABC):
    @staticmethod
    def get(name: str):
        if name == 'yolo':
            return tools.models.object_detectors.yolo.bus_detection.BusDetection()
        else:
            raise RuntimeError('Wrong detector name')
