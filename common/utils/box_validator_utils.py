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
        Match text from text box with usual number naming REGEXP: Check if recognized text matches with one of
        templates. TEMPLATES: 1) Any character + any digits ( count of digits should be in limit from 1 to 3),
        example: A43, T1, Z072. Incorrect Example: TQ12, A1234, 12A 2) Any digits ( count of digits should be in limit
        from 1 to 3). Example: 97, 103, 123.  Incorrect Example: 1234
        :param text_box: input text box
        :return: True if matched
        """
        return re.match(r'(^[a-zA-Zа-яА-Я]\d{1,3}$)|(^\d{1,3}$)', text_box.text)

