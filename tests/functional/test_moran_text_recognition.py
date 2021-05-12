from tools.models.text_recognizers.moran.recongition_interface import RecognitionInterface
from tests.checkers.test_checker import Accuracy
import cv2
import pytest


class TestMoranTextRecognition:
    def test_can_recognize_text(self):
        recognizer = RecognitionInterface()
        image = cv2.imread('./test_data/text_sample.png')
        text = recognizer.run_recognition(image)

    # TODO: Need add fixture
    @pytest.skip("Need add data")
    def test_check_text_recognition(self):
        recognizer = RecognitionInterface()
        images_path = Accuracy.get_test_image_text('./tests/checkers/data_text.txt')
        for image_str in images_path:
            image = cv2.imread(image_str[0])
            text = recognizer.run_recognition(image)
            Accuracy.check_text_recognition(text, image_str[1])

