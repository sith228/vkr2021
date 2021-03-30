from urllib.request import urlopen

import numpy as np
import cv2

import requests


def download_image(pic_url):
    response = requests.get(pic_url, stream=True)
    if not response.ok:
        print("Download image", response)

    req = urlopen(pic_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def resize_to_show(img, width=300):
    s = img.shape[:2]; asp_rat = s[0] / s[1]; height = int(width * asp_rat)
    return cv2.resize(img, (width, height))


def show_image(img, name="Debug", pause=1, width=300):
    cv2.imshow(name, resize_to_show(img, width))
    cv2.waitKey(pause)
