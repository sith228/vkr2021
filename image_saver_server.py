import os
from datetime import datetime

import cv2
import time
import copy
import argparse
import numpy as np
from flask import Flask, request, Response
from urllib.request import Request, urlopen
import logging
import logging.config
from tools.text_detection.text_detection import TextDetector
from tools.text_recognition.text_recognition import TextRecognition

from tools.recongition_interface import moran_demo as moran_recognizer


def init_arg_parser():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("port", type=int, action="store", choices=range(0, 65535), help="Server port number")

    # Optional arguments
    parser.add_argument("-detector", default="default", type=str, action="store", choices=["default"], help="Text detection network")
    parser.add_argument("-recognizer", default="moran",  type=str, action="store", choices=["default", "moran"], help="Text recognition network")
    parser.add_argument("-debug", action="store_true")
    return parser

def init_logger():
    logger_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '[%(asctime)s:%(msecs)03d] %(levelname)-5s %(message)s',
                'datefmt': '%d.%m %H:%M:%S',
            }, 'net': {
                'format': '%(asctime)s %(message)s',
                'datefmt': '%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'summary': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': "test_summary.log",
                'encoding': 'utf-8',
                'mode': 'w',
                'formatter': 'default'
            }
        },
        'loggers': {
            'main': {
                'handlers': ['summary', 'console'],
                'level': 'DEBUG',
                'propagate': True
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'summary']
        }
    }

    logging.config.dictConfig(logger_config)


init_logger()
log = logging.getLogger("root")
log.info("Hello")


class Server(object):
    def __init__(self, args):
        # setup Flask
        self.app = Flask(__name__)
        self.init_flask()
        self.port = args.port
        self.debug = args.debug
        self.output_dir = None

    def init_flask(self):
        """

        Rules for apply get request.

        """
        # Get image handler
        self.app.add_url_rule('/save_image', 'save_image', lambda: Response(self.save_image()),
                              methods=['GET', 'POST'])

    def save_image(self):
        image = np.fromstring(request.data, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        answer = " "

        # box detection and text recognition
        detector = TextDetector()
        recognitor = TextRecognition()
        boxes = detector.get_boxes(image, 0, 0)

        temp = copy.copy(image)
        number_plate = None
        for i in range(len(boxes)):
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
                    cv2.imwrite(self.output_dir + "/debug/" + datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S[') + str(i) + "].jpg", part)

                # Part checking
                if i == 0:
                    number_plate = part
                part = cv2.resize(part, (120, 32))
                # part = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
                # sign = TextRecognition.run_recognition(part, None, recognitor.run_vino_recognition)
                sign = moran_recognizer(part)
                if i == 0:
                    answer = sign
                if not sign == "text":
                    cv2.putText(temp, sign, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)
                cv2.rectangle(temp, (x1, y1), (x2, y2), (0, 0, 255), 2)

        time = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')
        log.info(time)
        file_name = "{}.jpg".format(time)

        if number_plate is not None:
            cv2.imwrite(os.path.join("test_numbers", file_name), number_plate)

        image = temp

        if self.debug:
            cv2.imshow("img", cv2.resize(image, (400 * 3, 300 * 3)))
            cv2.waitKey()

        result = cv2.imwrite(os.path.join(self.output_dir, file_name), image)
        log.info("Save result: {}".format(result))
        return answer

    def run(self):
        output_dir = os.path.join("files")
        os.makedirs(output_dir, exist_ok=True)
        if os.path.exists(output_dir):
            self.output_dir = os.path.abspath(output_dir)
            log.info("Save directory created: {}".format(self.output_dir))
        if self.debug:
            os.makedirs(self.output_dir + "/debug", exist_ok=True)
        self.app.run(host="0.0.0.0", port=self.port, threaded=True)


arg_parser = init_arg_parser()
args = arg_parser.parse_args()

s = Server(args)
s.run()
