import re

from common.box import TextBox


class BoxValidator:
    def __init__(self):
        self.max_aspect_ratio = 2

    def size_validation(self, box) -> bool:
        """
        Check if aspect ratio is acceptable
        :param box: Box
        :return: True if aspect ratio is acceptable
        """
        width = box[1][0] - box[0][0]
        height = box[1][1] - box[0][1]
        if (width / height > self.max_aspect_ratio) or (height / width > self.max_aspect_ratio):
            return False
        return True

    @staticmethod
    def has_valid_text(text_box: TextBox):  # TODO: Only for Nizniy Novgorod
        return re.match('\\d*', text_box.get_text())

