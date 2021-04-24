import numpy as np


class Data:
    @staticmethod
    def decode_image(data: bytes) -> np.ndarray:
        height = int.from_bytes(data[0:2], 'little')
        width = int.from_bytes(data[2:4], 'little')
        image_format = 0  # TODO: Decode image format
        return np.frombuffer(data[5:], np.uint8).reshape((height, width))  # TODO: Use image format information
