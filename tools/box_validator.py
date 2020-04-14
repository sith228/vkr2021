class BoxValidator:
    def __init__(self):
        self.max_aspect_ratio = 2

    def size_validation(self, box):
        width = box[1][0] - box[0][0]
        height = box[1][1] - box[0][1]
        if (width / height > self.max_aspect_ratio) or (height / width > self.max_aspect_ratio):
            return False
        return True
