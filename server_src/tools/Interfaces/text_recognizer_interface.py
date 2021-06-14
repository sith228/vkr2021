from abc import ABC, abstractmethod
from typing import AnyStr


class ITextRecognizer(ABC):
    @abstractmethod
    def prediction(self, image):
        raise NotImplementedError

    @abstractmethod
    def get_result(self) -> AnyStr:
        raise NotImplementedError
