from typing import List
import cv2

from common.box import Box
from common.bus_box import BusBox
from common.text_box import TextBox
from common.door_box import DoorBox


class TestBox:
    def test_create_Box(self):
        image = cv2.imread('./test_data/text_sample.png')
        box: Box = Box([1, 1], 10, 10, image.view())
        assert box
        assert len(box.get_crop_image())

    def test_insert_and_get_Boxes(self):
        image = cv2.imread('./test_data/text_sample.png')
        box = Box([1, 1], 10, 10, image.view())
        boxes = [Box([1, 1], 10, 10, image.view()), Box([1, 1], 10, 10, image.view())]
        box.insert_box(boxes)
        assert len(box.get_subboxes()) == 2
        assert box.get_subboxes()[0] is boxes[0]

    def test_create_some_boxes(self):
        image = cv2.imread('./test_data/text_sample.png')
        boxes: List[Box] = [BusBox((1, 1), 10, 10, image.view()), DoorBox((1, 1), 10, 10, image.view()),
                            TextBox((1, 1), 10, 10, image.view(), 'test')]
        for box in boxes:
            assert len(box.get_crop_image())
        assert len(boxes) == 3
