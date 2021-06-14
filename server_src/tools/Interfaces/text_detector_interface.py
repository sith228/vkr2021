from abc import ABC, abstractmethod
from typing import List
from common.box import Box


class ITextDetector(ABC):
    @abstractmethod
    def prediction(self, image):
        raise NotImplementedError

    @abstractmethod
    def get_boxes(self) -> List[Box]:
        raise NotImplementedError
