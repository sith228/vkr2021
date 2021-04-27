import time
from typing import List
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
    def check_boxes(boxes: List[Box]):
        pass
