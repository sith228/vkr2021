import cv2
import pytest

from tools.models.text_detectors.craft.text_craft_detector import CraftDetection


class TestCraftDetector:
    @pytest.mark.skip
    def test_craft_detector_on_cpu(self):
        craft = CraftDetection(cuda=False)
        image = cv2.imread('./test_data/text_sample.png')
        craft.prediction(image)
        prediction_result = craft.get_boxes()
        assert prediction_result

