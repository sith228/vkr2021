from common.box import Box


class TestBox:
    def test_create_Box(self):
        box = Box([1, 1], 10, 10, 0)
        assert box

    def test_insert_and_get_Boxes(self):
        box = Box([1, 1], 10, 10, 0)
        boxes = [Box([1, 1], 10, 10, 0), Box([1, 1], 10, 10, 0)]
        box.insert_box(boxes)
        assert len(box.get_subboxes()) == 2
        assert box.get_subboxes()[0] is boxes[0]
