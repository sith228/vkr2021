import os
from datetime import datetime

import cv2
import copy
import numpy as np

from response_callbacks.callback import Callback
from tools.box_validator import BoxValidator
from tools.models.moran_text_recognition.recongition_interface import RecognitionInterface
from tools.models.openvino_text_detection.text_detection import OVTextDetector
from tools.models.openvino_vehicle_detection.vehicle_detection import OVVehicleDetector


class BusDetectionPipeline(Callback):
    def __init__(self, output_dir, debug=False):
        super().__init__()
        self.debug = debug
        self.output_dir = output_dir

        # box detection and text recognition
        self.vehicle_detector = OVVehicleDetector()
        self.text_detector = OVTextDetector()
        self.text_recognizer = RecognitionInterface()
        self.validator = BoxValidator()

    def get_text_boxes(self, vehicle_boxes, image, temp):
        """

        :param vehicle_boxes:
        :param image:
        :param temp:
        :return:
        """
        boxes = []
        for box in vehicle_boxes:
            ymin = box[0][1]
            ymax = box[1][1]
            xmin = box[0][0]
            xmax = box[1][0]
            temp_boxes = self.text_detector.get_boxes(image[ymin:ymax, xmin:xmax], 0, 0)
            for temp_box in temp_boxes:
                x1 = temp_box.bound_box_points[0][0]
                x2 = temp_box.bound_box_points[1][0]
                y1 = temp_box.bound_box_points[0][1]
                y2 = temp_box.bound_box_points[1][1]
                boxes.append([[x1 + xmin, y1 + ymin], [x2 + xmin, y2 + ymin]])
            if self.debug:
                cv2.rectangle(temp, (xmin, ymin), (xmax, ymax), (255, 255, 0), 2)
        return boxes

    def get_plate_number(self, image, text_boxes, temp):

        named = False
        answer = ""
        for i, box in enumerate(text_boxes):
            if not self.validator.size_validation(box):
                continue
            x1 = box[0][0]
            x2 = box[1][0]
            x_indent = int((x2 - x1) / 10)
            x1 = max(x1 - x_indent, 0)
            x2 = x2 + x_indent
            y1 = box[0][1]
            y2 = box[1][1]
            y_indent = int((y2 - y1) / 10)
            y1 = max(y1 - y_indent, 0)
            y2 = y2 + y_indent
            part = image[y1:y2, x1:x2]

            if x1 < x2 and y1 < y2:
                text = self.text_recognizer.run_recognition(part)
                if not named:
                    answer = text
                    named = True
                if not text == "text":
                    cv2.putText(temp, text, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
                    cv2.rectangle(temp, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.imwrite(self.output_dir + "/debug/" + datetime.utcnow().
                                strftime('%Y-%m-%d %H-%M-%S[') + str(i) + "].jpg", temp)
        return answer

    def startProcessing(self, data) -> dict:
        image = np.fromstring(data, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        vehicle_boxes = self.vehicle_detector.get_boxes(image)
        self.log.info("Veichels = %d", len(vehicle_boxes))

        temp = copy.copy(image)
        boxes = self.get_text_boxes(vehicle_boxes, image, temp)
        answer = self.get_plate_number(image, boxes, temp)

        time = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')
        self.log.info(time)
        file_name = "{}.jpg".format(time)

        if self.debug:
            cv2.imshow("img", cv2.resize(image, (400 * 3, 300 * 3)))
            cv2.waitKey()

        result = cv2.imwrite(os.path.join(self.output_dir, file_name), image)
        self.log.info("Save result: {}".format(result))
        return answer
