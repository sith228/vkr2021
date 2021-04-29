import time
import cv2
from tools.models.object_detectors.yolo.bus_detection import BusDetection
from typing import Tuple, List
from common.box.box import Box


class Performance:
    @staticmethod
    def check(function) -> float:
        start = time.time()
        function()
        end = time.time() - start
        return end


class Accuracy:
    @staticmethod
    def get_test_image():
        data = []
        results_data = []
        with open('./tests/checkers/data.txt', 'r') as f:
            for line in f:
                data.append(line)

        for file_box in data:
            result = file_box.split(' ')
            text = result[0]
            if len(result) > 5:
                text = text + ' ' + result[1]

            shape = result[-4:]
            for i, cord in enumerate(shape):
                shape[i] = int(cord)
            results_data.append((text, shape))
        return results_data

    @staticmethod
    def check_boxes(boxes: List[Tuple[str, Box]]):
        results_data = Accuracy.get_test_image()

        for box_candidate in boxes:
            for next_data in results_data:
                if next_data[0] == box_candidate[0]:
                    image = cv2.imread(next_data[0])
                    result_box = Box((next_data[1][0], next_data[1][1]), next_data[1][2], next_data[1][3], image)
                    assert Box.check_intersection(result_box, box_candidate[1])
                    assert Box.compare_boxes(result_box, box_candidate[1]) > 0.5
