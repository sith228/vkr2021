from typing import List, Mapping

import cv2
import numpy as np

from common.box import BusBox
from server.network.image_format import ImageFormat


class Data:
    @staticmethod
    def decode_image(data: bytes) -> np.ndarray:
        """
        Decodes image from packet data
        :param data: packet data
        :return: Image
        """
        height = int.from_bytes(data[0:2], 'little')
        width = int.from_bytes(data[2:4], 'little')
        image_format = ImageFormat(int.from_bytes(data[4:5], 'little', signed=False))
        if image_format == ImageFormat.RAW_BGR:
            return np.frombuffer(data[5:], np.uint8).reshape((height, width, 3))
        elif image_format == ImageFormat.JPG_RGB:
            return cv2.imdecode(np.frombuffer(data[5:], np.uint8), cv2.IMREAD_COLOR)

    @staticmethod
    def encode_image(image: np.ndarray, image_format: ImageFormat) -> bytes:
        """
        Returns packet data from image
        :param image: image
        :param image_format: image format
        :return: packet data
        """
        result = b''
        result += (image.shape[0]).to_bytes(2, 'little')
        result += image.shape[1].to_bytes(2, 'little')
        result += image_format.value.to_bytes(1, 'little', signed=False)
        if image_format == ImageFormat.RAW_BGR:
            result += image.tobytes()
        elif image_format == ImageFormat.JPG_RGB:
            result += cv2.imencode('.jpg', image)[1].tobytes()
        return result

    @staticmethod
    def encode_bus_boxes(bus_boxes: List[BusBox]):
        """
        Encode packet data from bus boxes
        :param bus_boxes: List of bus boxes
        :return: Packet data
        """
        result = b''
        result += int(0).to_bytes(1, 'little')  # TODO: Add control
        for bus_box in bus_boxes:
            bound_box = bus_box.get_bound_box()
            result += bound_box[0].to_bytes(4, 'little')  # x
            result += bound_box[1].to_bytes(4, 'little')  # y
            result += bound_box[2].to_bytes(4, 'little')  # Height
            result += bound_box[3].to_bytes(4, 'little')  # Width
            if bus_box.route_number is not None:
                result += len(bus_box.route_number).to_bytes(4, 'little')  # Text length
                result += bus_box.route_number.encode()  # Text
            else:
                result += int(0).to_bytes(4, 'little')  # Text length

        return result

    @staticmethod
    def decode_bus_boxes(data: bytes) -> Mapping:
        result_packet = {'control': int.from_bytes(data[0:1], 'little'), 'x': int.from_bytes(data[1:5], 'little'),
                         'y': int.from_bytes(data[5:9], 'little'), 'height': int.from_bytes(data[9:13], 'little'),
                         'width': int.from_bytes(data[13:17], 'little'),
                         'text_size': int.from_bytes(data[17:21], 'little')}
        result_packet['text'] = data[21:21+result_packet['text_size']].decode()
        return result_packet
