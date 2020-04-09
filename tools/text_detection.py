from tools.models.openvino_text_detection.text_detection import OVTextDetector
from tools.models.craft_text_segmentation.craft import CRAFT


class TextDetection(object):
    def __init__(self):
        self.openvino_td = OVTextDetector()
        self.craft_td = CRAFT()
