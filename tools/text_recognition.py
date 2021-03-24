from tools.models.openvino_text_recognition.text_recognition import OVTextRecognition
from tools.models.moran_text_recognition.recongition_interface import RecognitionInterface


class TextRecognition(object):
    def __init__(self):
        self.moron_tr = RecognitionInterface()
        self.openvino_tr = OVTextRecognition()
