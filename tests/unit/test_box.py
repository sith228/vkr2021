from typing import List

from common.box import Box
from common.bus_box import BusBox
from common.text_box import TextBox
from common.door_box import DoorBox


class TestBox:
    def test_create_Box(self):
        box = Box([1, 1], 10, 10)
        assert box

    def test_insert_and_get_Boxes(self):
        box = Box([1, 1], 10, 10)
        boxes = [Box([1, 1], 10, 10), Box([1, 1], 10, 10)]
        box.insert_box(boxes)
        assert len(box.get_subboxes()) == 2
        assert box.get_subboxes()[0] is boxes[0]

    def test_create_some_boxes(self):
        boxes: List[Box] = [BusBox((1, 1), 10, 10), DoorBox((1, 1), 10, 10), TextBox((1, 1), 10, 10, 'test')]
        assert len(boxes) == 3
