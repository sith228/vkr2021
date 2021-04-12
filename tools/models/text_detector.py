from abc import ABC
import torch

from tools.models.text_detectors.craft.text_craft_detector import CraftDetection


class TextDetectorFactory(ABC):
    @staticmethod
    def get(name: str):
        if name == 'craft':
            if torch.cuda.is_available():
                return CraftDetection(True)
            else:
                return CraftDetection(False)
        else:
            raise RuntimeError('Wrong detector name ' + name)
