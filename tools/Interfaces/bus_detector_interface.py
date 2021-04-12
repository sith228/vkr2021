from abc import ABC, abstractmethod
from typing import List
from common.box import Box


class IBusDetector(ABC):

    @abstractmethod
    def prediction(self, img):
        pass

    @abstractmethod
    def get_boxes(self) -> List[Box]:
        pass
