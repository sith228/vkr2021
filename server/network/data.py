from typing import List

import numpy as np

from common.box import BusBox
from server.network.image_format import ImageFormat


class Data:
    @staticmethod
    def decode_image(data: bytes) -> np.ndarray:
        height = int.from_bytes(data[0:2], 'little')
        width = int.from_bytes(data[2:4], 'little')
        image_format = ImageFormat(int.from_bytes(data[4:5], 'little', signed=False))
        if image_format == ImageFormat.RAW_BGR:
            return np.frombuffer(data[5:], np.uint8).reshape((height, width, 3))

    @staticmethod
    def encode_image(image: np.ndarray, image_format: ImageFormat):
        result = b''
        result += (image.shape[0]).to_bytes(2, 'little')
        result += image.shape[1].to_bytes(2, 'little')
        result += image_format.value.to_bytes(1, 'little', signed=False)
        if image_format == ImageFormat.RAW_BGR:
            result += image.tobytes()
        return result

    @staticmethod
    def encode_bus_boxes(bus_boxes: List[BusBox]):
        result = b''
        result += int(0).to_bytes(1, 'little')  # TODO: Add control
        for bus_box in bus_boxes:
            bound_box = bus_box.get_bound_box()
            result += bound_box[0].to_bytes(4, 'little')
            result += bound_box[1].to_bytes(4, 'little')
            result += bound_box[2].to_bytes(4, 'little')
            result += bound_box[3].to_bytes(4, 'little')
            result += int(0).to_bytes(4, 'little')  # TODO: Add text
        return result
