import os
from datetime import datetime

import cv2
import copy
import numpy as np

from response_callbacks.callback import Callback
from tools.box_validator import BoxValidator
from tools.models.moran_text_recognition.recongition_interface import RecognitionInterface
from tools.models.openvino_text_detection.text_detection import OVTextDetector


class LowRes(Callback):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        self.output_dir = "files"

    def startProcessing(self, data) -> dict:
        image = np.fromstring(data, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        answer = " "

        # box detection and text recognition
        detector = OVTextDetector()
        recognizer = RecognitionInterface()
        validator = BoxValidator()
        boxes = detector.get_boxes(image, 0, 0)

        temp = copy.copy(image)
        number_plate = None
        for i in range(len(boxes)):
            if not validator.size_validation(boxes[i]):
                continue
            x1 = boxes[i].box_points[0][0]
            x2 = boxes[i].box_points[2][0]
            x_indent = int((x2 - x1) / 10)
            x1 = x1 - x_indent
            x2 = x2 + x_indent
            y1 = boxes[i].box_points[0][1]
            y2 = boxes[i].box_points[2][1]
            y_indent = int((y2 - y1) / 10)
            y1 = y1 - y_indent
            y2 = y2 + y_indent
            part = image[y1:y2, x1:x2]

            if x1 < x2 and y1 < y2:
                if self.debug:
                    cv2.imwrite(self.output_dir + "/debug/" + datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S[') + str(i)
                                + "].jpg", part)

                # Part checking
                if i == 0:
                    number_plate = part
                part = cv2.resize(part, (120, 32))
                # part = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
                # sign = TextRecognition.run_recognition(part, None, recognitor.run_vino_recognition)
                sign = recognizer.run_recognition(part)
                if i == 0:
                    answer = sign
                if not sign == "text":
                    cv2.putText(temp, sign, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)
                cv2.rectangle(temp, (x1, y1), (x2, y2), (0, 0, 255), 2)

        time = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')
        self.log.info(time)
        file_name = "{}.jpg".format(time)

        if number_plate is not None:
            cv2.imwrite(os.path.join("test_numbers", file_name), number_plate)

        image = temp

        if self.debug:
            cv2.imshow("img", cv2.resize(image, (400 * 3, 300 * 3)))
            cv2.waitKey()

        result = cv2.imwrite(os.path.join(self.output_dir, file_name), image)
        self.log.info("Save result: {}".format(result))
        return answer
