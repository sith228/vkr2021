from abc import ABC


class TextRecognizerFactory(ABC):
    @staticmethod
    def get(name: str):
        pass
