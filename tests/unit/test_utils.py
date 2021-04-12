import os
import cv2
import pytest
import numpy as np

from common.utils.box_validator_utils import BoxValidator
from common.utils.os_utils import OsUtil
from common.utils.opencv_inference import OpenCvInference
from common.utils.recognition_utils import RecognitionUtils
from common.utils.image_utils import resize_to_show


# TODO: Added tests for utils

class TestsUtils:
    def test_can_validate_size(self):
        validator = BoxValidator()
        assert validator.size_validation([[0, 0], [1, 1]]) is True

    def test_os_utils(self):
        assert (OsUtil.is_linux() or not OsUtil.is_linux())
        assert (OsUtil.is_windows() or not OsUtil.is_windows())
        assert (OsUtil.is_macos() or not OsUtil.is_macos())

    @pytest.mark.skip
    def test_opencv_inference(self):
        model_xml = os.path.join("tools", "models", "openvino", "vehicle-detection-adas-0002.xml")
        model_bin = os.path.join("tools", "models", "openvino", "vehicle-detection-adas-0002.bin")
        image = cv2.imread('./test/text_sample.png')

        opencv_inference = OpenCvInference(model_xml, model_bin, 384, 672)
        assert opencv_inference.inference_sync(image)

    def test_recognition_utils(self):
        test_array = np.zeros([30, 37])
        assert RecognitionUtils.decode_sequence(test_array)

    def test_resize_to_show(self):
        test_array = np.zeros([900, 900])
        test_array = resize_to_show(test_array)
        assert test_array.shape[0] == 300 and test_array.shape[1] == 300

