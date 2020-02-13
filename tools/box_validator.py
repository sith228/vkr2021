class BoxValidator:
    def __init__(self):
        self.max_aspect_ratio = 2

    def size_validation(self, box):
        width = box.box_points[2][0] - box.box_points[0][0]
        height = box.box_points[2][1] - box.box_points[0][1]
        if (width / height > self.max_aspect_ratio) or (height / width > self.max_aspect_ratio):
            return False
        return True
