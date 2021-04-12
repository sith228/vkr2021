from abc import ABCMeta, abstractmethod
from typing import List
from common.box import Box
import zope.interface

import numpy as np


class IBusDetector(zope.interface.Interface):

    def prediction(self, img):
        pass

    def get_boxes(self) -> List[Box]:
        pass
