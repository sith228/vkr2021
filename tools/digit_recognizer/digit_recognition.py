import numpy as np
import cv2
import os


import time

from keras.models import load_model


class DigitRecognition(object):
    decoder = {
        0: 8,
        1: 0,
        2: 1,
        3: 3,
        4: 9,
        5: 5,
        6: 4,
        7: 2,
        8: 7,
        9: 6
    }

    # load models
    def __init__(self, threshold=0.65):
        super().__init__()

        self.name = 0
        self.threshold = threshold
        dirpath = os.getcwd()
        print("dirpath")
        print(dirpath)
        if os.path.basename(dirpath) != "digit_recognizer":
            path_to_model = os.path.join(dirpath, "tools", "digit_recognizer", "weights_weights_DNN_0.hdf5")
        else:
            path_to_model = os.path.join("weights_weights_DNN_0.hdf5")
        print(path_to_model)
        print(os.path.exists(path_to_model))

        self.model = load_model(path_to_model)

        self.h = 48
        self.w = 48
        self.c = 3

    def run_recognition(self, roi):
        start_time = time.time()
        roi = roi.astype('float32') / 255.0
        out = self.model.predict_proba(roi.reshape(1, self.h, self.w, self.c))
        print((time.time() - start_time)*1e+3, " digit-recognition-001 runtime")
        print(out.max(), DigitRecognition.decoder[out.argmax()])
        if self.threshold < out.max():
            return DigitRecognition.decoder[out.argmax()], out.max()
        return "text", 0.8


if __name__ == '__main__':
    text_recognition = DigitRecognition()
    image = cv2.imread("/Users/danreegly/Downloads/6(2).jpg")
    try:
        o = text_recognition.run_recognition(cv2.resize(image, (48, 48)))
        print(o)
    except Exception as e:
        pass
