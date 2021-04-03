from __future__ import print_function
import os
import cv2
from utils.inference_engine import InferenceEngine


# TODO: change realization to with IE utils.
class OVVehicleDetector:
    def __init__(self):
        model_xml = os.path.join("tools", "models", "openvino_vehicle_detection", "vehicle-detection-adas-0002.xml")
        model_bin = os.path.join("tools", "models", "openvino_vehicle_detection", "vehicle-detection-adas-0002.bin")

        self.ie = InferenceEngine(xml_path=model_xml, bin_path=model_bin)
        self.n, self.c, self.h, self.w = self.ie.net.inputs["data"].shape
        self.inference = self.ie.inference_sync

    def get_boxes(self, image, threashold=0.5):
        result = self.inference(cv2.resize(image, (self.h, self.w)))
        boxes = []
        for obj in result[0][0]:
            if obj[2] > threashold:
                xmin = int(obj[3] * self.w)
                ymin = int(obj[4] * self.h)
                xmax = int(obj[5] * self.w)
                ymax = int(obj[6] * self.h)
                boxes.append([[xmin, ymin], [xmax, ymax]])
        return boxes
