import re

from common.box import TextBox


class BoxValidator:
    def __init__(self):
        self.max_aspect_ratio = 2

    # TODO: update for new box
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
    def has_valid_text(text_box: TextBox):
        """
        Match text from text box with usual number naming
        :param text_box: input text box
        :return: True if matched
        """
        return re.match(r'(^[a-zA-Zа-яА-Я]\d\d{,2}$)|(^\d\d{,2}$)', text_box.text)

