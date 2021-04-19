from typing import List
import cv2

from . import Box
from . import BusBox
from . import TextBox
from . import DoorBox


class TestBox:
    def test__can_create_box(self):
        image = cv2.imread('./test_data/text_sample.png')
        box: Box = Box([1, 1], 10, 10, image.view())
        assert box
        assert len(box.get_cropped_image())

    def test_can_insert_and_get_boxes(self):
        image = cv2.imread('./test_data/text_sample.png')
        box = Box([1, 1], 10, 10, image.view())
        boxes = [Box([1, 1], 10, 10, image.view()), Box([1, 1], 10, 10, image.view())]
        box.insert_boxes(boxes)
        assert len(box.get_subboxes()) == 2
        assert box.get_subboxes()[0] is boxes[0]

    def test_can_create_some_boxes(self):
        image = cv2.imread('./test_data/text_sample.png')
        boxes: List[Box] = [BusBox((1, 1), 10, 10, image.view()), DoorBox((1, 1), 10, 10, image.view()),
                            TextBox((1, 1), 10, 10, image.view(), 'test')]
        for box in boxes:
            assert len(box.get_cropped_image())
        assert len(boxes) == 3
