from abc import ABC

from tools.Interfaces.text_recognizer_interface import ITextRecognizer
from tools.models.text_recognizers.moran.moran import MoranTextRecognizer


class TextRecognizerFactory(ABC):
    @staticmethod
    def get(name: str) -> ITextRecognizer:
        if name == 'moran':
            return MoranTextRecognizer()
