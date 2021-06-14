import cv2
import numpy as np


def resize_to_show(image: np.ndarray, width: int = 300) -> np.ndarray:
    """
    Resizes image with keeping aspect ratio
    :param image: Input image
    :param width: Target width
    :return: Result image
    """
    s = image.shape[:2]
    asp_rat = s[0] / s[1]
    height = int(width * asp_rat)
    return cv2.resize(image, (width, height))


def show_image(image: np.ndarray, name: str = 'Debug', pause: int = 1, width: int = 300):
    """
    Shows image at screen
    :param image: Input image
    :param name: Window name
    :param pause: Pause to show window
    :param width: Window width
    :return:
    """
    cv2.imshow(name, resize_to_show(image, width))
    cv2.waitKey(pause)
