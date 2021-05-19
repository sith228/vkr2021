import time
import cv2
import re
from typing import Tuple, List
from common.box.text_box import Box, TextBox
from common.logger import init_logger

import logging


class Performance:
    @staticmethod
    def check(function) -> float:
        """
        Returns speed for function
        :param function:
        :return: milliseconds
        """
        start = time.time()
        function()
        end = time.time() - start
        return end


class Accuracy:
    # TODO: Need to make a general solution for dump names
    @staticmethod
    def get_test_image(file: str):
        """
        Returns list of names for testing
        :param file:
        :return: ist of names
        """
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

    # TODO: Need to make a general solution for dump names
    @staticmethod
    def get_test_image_text(file: str):
        """
        Returns list of names for testing
        :param file:
        :return: ist of names
        """
        data = []
        results_data = []
        with open(file, 'r') as f:
            for line in f:
                data.append(line)

        for file_box in data:
            result = file_box.split(' ')
            if result[1][-1] == '\n':
                result[1] = result[1][:-1]
            text = result[0]

            results_data.append((text, result[1]))
        return results_data

    # TODO: Need add logging data
    @staticmethod
    def check_boxes(boxes: List[Tuple[str, Box]]):
        """
        Checks that boxes intersect with tests boxes more than 50%
        :param boxes: Boxes which had been detected
        :return: none
        """
        logger = logging.getLogger('tests')
        results_data = Accuracy.get_test_image('./tests/checkers/data.txt')

        for box_candidate in boxes:
            for next_data in results_data:
                if next_data[0] == box_candidate[0]:
                    image = cv2.imread(next_data[0])
                    result_box = Box((next_data[1][0], next_data[1][1]), next_data[1][2], next_data[1][3], image)
                    logger.info('Name image' + next_data[0])
                    logger.info('Intersection: ' + str(Box.check_intersection(result_box, box_candidate[1])))
                    logger.info('Compare Box: ' + str(Box.compare_boxes_area(result_box, box_candidate[1])))

    @staticmethod
    def check_text_recognition(text_rec: str, text_check: str) -> float:
        """
        Checks correct recognition text
        :param text_rec: Text which had been recognized
        :param text_check: Texts in test file
        :return: Percent of correct
        """
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
    def check_text_box(text_box: Tuple[str, List[TextBox]], data: str):
        logger = logging.getLogger('tests')
        result_data = Accuracy.get_test_image(data)
        all_images = 0
        do_match: bool = False
        accuracy_recognition: float = 0.0
        for next_data in result_data:
            if next_data[0] == text_box[0]:
                image = cv2.imread(next_data[0])
                result_box = Box((next_data[1][0], next_data[1][1]), next_data[1][2], next_data[1][3], image)
                for test_box in text_box[1]:
                    all_images = all_images + 1
                    if Box.check_intersection(test_box, result_box):
                        if Box.compare_boxes_area(test_box, result_box):
                            if Accuracy.check_text_recognition(test_box.text, next_data[2]) > 0.75:
                                accuracy_recognition = Accuracy.check_text_recognition(test_box.text, next_data[2])
                                do_match = True
        logger.info('WAS MATCH: ' + str(do_match))
        if do_match:
            logger.info('Precision = ' + str(float(1 / all_images)))
            logger.info('Accuracy = ' + str(accuracy_recognition))
            return do_match, float(1 / all_images), accuracy_recognition
        else:
            logger.info('Precision = 0')
            logger.info('Accuracy = 0')
            return do_match, 0, 0.0
