import cv2

from tools.models.text_detectors.craft.text_craft_detector import CraftDetection


class TestCraftDetector:
    def test_craft_detector_on_cpu(self):
        craft = CraftDetection(cuda=False)
        image = cv2.imread('./test_data/text_sample.png')
        craft.prediction(image)
        prediction_result = craft.get_boxes()
        assert prediction_result

