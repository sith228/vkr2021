from abc import ABC, abstractmethod
from typing import List
from common.box import Box


class IBusDetector(ABC):

    @abstractmethod
    def prediction(self, img):
        raise NotImplementedError

    @abstractmethod
    def get_boxes(self) -> List[Box]:
        raise NotImplementedError
