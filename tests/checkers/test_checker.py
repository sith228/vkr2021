import time
import cv2
import re
import numpy as np
from typing import Tuple, List
from common.box.text_box import Box, TextBox



class Performance:
    @staticmethod
    def check(function) -> float:
        start = time.time()
        function()
        end = time.time() - start
        return end


class Accuracy:
    @staticmethod
    def get_test_image(file: str):
        data = []
        results_data = []
        with open(file, 'r') as f:
            for line in f:
                data.append(line)

        for file_box in data:
            result = file_box.split(' ')
            text = result[0]
            result_value: str = ''
            if len(result) > 5:
                text_match = re.search(r'(^[a-zA-Zа-яА-Я]\d*$)|(^\d*$)', result[1])
                if text_match:
                    result_value = result[1]
                else:
                    text = text + ' ' + result[1]
            if len(result) > 6:
                text_match = re.search(r'(^[a-zA-Zа-яА-Я]\d*$)|(^\d*$)', result[2])
                if text_match:
                    result_value = result[2]

            shape = result[-4:]
            for i, cord in enumerate(shape):
                shape[i] = int(cord)
            results_data.append((text, shape, result_value))
        return results_data

    @staticmethod
    def check_boxes(boxes: List[Tuple[str, Box]]):
        results_data = Accuracy.get_test_image('./tests/checkers/data.txt')

        for box_candidate in boxes:
            for next_data in results_data:
                if next_data[0] == box_candidate[0]:
                    image = cv2.imread(next_data[0])
                    result_box = Box((next_data[1][0], next_data[1][1]), next_data[1][2], next_data[1][3], image)
                    assert Box.check_intersection(result_box, box_candidate[1])
                    assert Box.compare_boxes(result_box, box_candidate[1]) > 0.5

    @staticmethod
    def check_text_recognition(text_rec: str, text_check: str) -> float:
        if len(text_rec) == len(text_check):
            match = re.search(text_check, text_rec)
            if match:
                return 1.0
            else:
                return 0.0
        else:
            match = re.search(r'^[a-zA-Zа-яА-Я]\d*$', text_check)
            if match:
                text_match = re.search(r'^[a-zA-Zа-яА-Я]\d*$', text_rec)
                if text_match and text_match[0] == text_check:
                    return float(len(text_check) / len(text_rec))
                else:
                    return 0.0
            else:
                text_match = re.search(r'\d*$', text_rec)
                if text_match and text_match[0] == text_check:
                    return float(len(text_check) / len(text_rec))
                else:
                    return 0.0

    @staticmethod
    def check_text_box(text_box: Tuple[str, List[TextBox]]):
        result_data = Accuracy.get_test_image('./tests/checkers/data.txt')
        all_images = 0
        do_match: bool = False
        accuracy_recognition: float = 0.0
        for next_data in result_data:
            if next_data[0] == text_box:
                image = cv2.imread(next_data[0])
                result_box = Box((next_data[1][0], next_data[1][1]), next_data[1][2], next_data[1][3], image)
                for test_box in text_box[1]:
                    all_images = all_images + 1
                    if Box.check_intersection(test_box, result_box):
                        if Box.compare_boxes(test_box, result_box):
                            if Accuracy.check_text_recognition(test_box.get_text(), next_data[2]) > 0.75:
                                accuracy_recognition = Accuracy.check_text_recognition(test_box.get_text(), next_data[2])
                                do_match = True
        if do_match:
            return do_match, float(1 / all_images), accuracy_recognition
        else:
            return do_match, 0, 0.0
