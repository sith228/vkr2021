from abc import ABC, abstractmethod
from typing import List, AnyStr
from common.box import Box


class ITextDetector(ABC):
    @abstractmethod
    def prediction(self, image):
        pass

    @abstractmethod
    def get_boxes(self) -> List[Box]:
        pass


class ITextRecognizer(ABC):
    @abstractmethod
    def prediction(self, image):
        pass

    @abstractmethod
    def get_recognized_text(self) -> AnyStr:
        pass
