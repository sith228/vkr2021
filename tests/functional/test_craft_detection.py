import cv2

from tools.models.text_detectors.craft.text_craft_detector import CraftDetection
from tests.checkers.test_checker import Performance


class TestCraftDetector:

    @staticmethod
    def function_test():
        craft = CraftDetection(cuda=False)
        image = cv2.imread('./test_data/text_sample.png')
        craft.prediction(image)
        return craft.get_boxes()

    def test_craft_detector_on_cpu(self):
        prediction_result = self.function_test()
        assert Performance.check(self.function_test) > 0
        assert prediction_result

