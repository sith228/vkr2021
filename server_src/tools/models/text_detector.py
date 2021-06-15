from abc import ABC
import torch

from tools.models.text_detectors.craft.text_craft_detector import CraftDetection
# from tools.models.text_detectors.openvino.text_detection import OVTextDetector


class TextDetectorFactory(ABC):
    @staticmethod
    def get(name: str):
        if name == 'craft':
            if torch.cuda.is_available():
                return CraftDetection(True)
            else:
                return CraftDetection(False)
        if name == 'openvino':
            # return OVTextDetector()
            raise RuntimeError('Wrong detector name ' + name)
        else:
            raise RuntimeError('Wrong detector name ' + name)
