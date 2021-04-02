from tools.models.openvino_text_detection.text_detection import OVTextDetector
from craft_text_detector import Craft


class TextDetection(object):
    def __init__(self):
        self.openvino_td = OVTextDetector()
        self.craft_td = Craft()
