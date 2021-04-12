from abc import ABC


class TextDetectorFactory(ABC):
    @staticmethod
    def get(name: str):
        pass
