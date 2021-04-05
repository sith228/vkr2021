from typing import List

import torch
import cv2
from common.box import Box


class BusDetection(object):
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
        self.__results__ = None

    def prediction(self, img):
        self.__results__ = self.model(img, size=640)

    def result(self) -> List[Box]:
        result_bus = []
        for pred in self.__results__.pred:
            for *box, conf, cls in pred:
                label = f'{self.__results__.names[int(cls)]}'
                if label == "bus":
                    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                    result_bus.append(Box(c1, c2[0], c2[1]))

        return result_bus


def main():
    bus_detector = BusDetection()
    #Uncommented to test
    # for f in ['zidane.jpg', 'bus.jpg']:  # download 2 images
    #     print(f'Downloading {f}...')
    #     torch.hub.download_url_to_file('https://github.com/ultralytics/yolov5/releases/download/v1.0/' + f, f)

    img2 = cv2.imread('bus.jpg')[:, :, ::-1]  # OpenCV image (BGR to RGB)
    img_res = cv2.imread('bus.jpg')
    bus_detector.prediction(img2)
    for box in bus_detector.result():
        img_res = cv2.rectangle(img_res, box.bound_box_points, (box.width, box.height), (255, 0, 0), 3, cv2.LINE_AA)
        cv2.imshow("Test", img_res)
        cv2.waitKey()

    img2 = cv2.imread('zidane.jpg')[:, :, ::-1]  # OpenCV image (BGR to RGB)
    img_res = cv2.imread('zidane.jpg')
    bus_detector.prediction(img2)
    for box in bus_detector.result():
        img_res = cv2.rectangle(img_res, box.bound_box_points, (box.width, box.height), (255, 0, 0), 3, cv2.LINE_AA)
        cv2.imshow("Test", img_res)
        cv2.waitKey()

    # results.show()


if __name__ == "__main__":
    main()