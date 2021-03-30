import numpy as np
import cv2
import os


import time

from common.utils.recognition_utils import RecognitionUtils
from common.utils.opencv_inference import OpenCvInference
from common.utils.inference_engine import InferenceEngine

#TODO Rename file

class OVTextRecognition(RecognitionUtils):
    # load models
    def __init__(self, ie=True, threshold=0.5):
        super().__init__()

        self.name = 0
        self.threshold = threshold

        model_xml = os.path.join("tools", "text_recognition", "text-recognition-0012.xml")
        model_bin = os.path.join("tools", "text_recognition", "text-recognition-0012.bin")

        print(os.path.exists(model_bin))
        print(os.path.exists(model_xml))

        h = 32
        w = 120

        if not ie:
            self.opencv = OpenCvInference(model_xml, model_bin, w, h)
            self.inference = self.opencv.inference_sync
        else:
            self.ie = InferenceEngine(model_xml, model_bin, w, h)
            self.inference = self.ie.inference_sync

    def run_vino_recognition(self, roi):
        start_time = time.time()
        out = self.inference(roi)
        print((time.time() - start_time)*1e+3, " text-recognition-0012 runtime")
        a, b = RecognitionUtils.decode_sequence(out)
        is_num = True
        for i in b:
            if i <= self.threshold:
                is_num = False
        if is_num:
            return a
        return "text"  # TODO WHATA FUCK

    # @staticmethod
    def get_recognition_result(self, image, boxes, number_of_components):
        src_pts = np.array([[0, 0], [119, 0], [119, 31], [0, 31]], dtype=np.float32)
        for box in boxes:
            m, _ = cv2.findHomography(box.box_points, src_pts)
            roi = cv2.warpPerspective(image, m, (120, 32))
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            if number_of_components == 1:
                    k = 50
                    img = 255 - np.zeros((32, 120), dtype=np.uint8)
                    img[:32, :k] = cv2.resize(roi, (k, 32))
                    roi = img
            im_gray = cv2.GaussianBlur(roi, (3, 3), 0)
            _, roi = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # cv2.imwrite("{}.jpeg".format(str(self.name)), roi)
            self.name += 1
            OVTextRecognition.run_recognition(roi, box, self.run_vino_recognition)

        return boxes

    @staticmethod
    def run_recognition_holst_boxes(boxes, recognizer, name=""):
        for box in boxes:
            if box.holst is not None:
                if box.holst.size == 0:
                    continue
            # if name != "":
            #     cv2.imwrite("holst_rec_{}.jpeg".format(str(name)), box.holst)

            text = recognizer(cv2.resize(box.holst, (120, 32)))
            box.set_vino_text(text) if "vino" in str(recognizer) else box.set_tesseract_text(text)
            box.set_vino_check() if "vino" in str(recognizer) else box.set_tesseract_check()
        return boxes

    @staticmethod
    def run_recognition(roi, box, method, name=""):
        text = method(roi)
        return text


if __name__ == '__main__':
    text_recognition = OVTextRecognition()
    grey = cv2.cvtColor(cv2.imread(".\\1558983710.3989537.jpeg"), cv2.COLOR_BGR2GRAY)
    try:
        OVTextRecognition.run_recognition(grey, None, text_recognition.run_vino_recognition)
    except Exception as e:
        pass
