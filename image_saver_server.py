import os
from datetime import datetime

import cv2
import time
import numpy as np
from flask import Flask, request, Response
from urllib.request import Request, urlopen
import logging
import logging.config
from tools.text_detection.text_detection import TextDetector
from tools.text_recognition.text_recognition import TextRecognition


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
    def __init__(self, _port):
        # setup Flask
        self.app = Flask(__name__)
        self.init_flask()
        self.port = _port
        self.debug = False
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

        # box detection and text recognition
        detector = TextDetector()
        recognitor = TextRecognition()
        boxes = detector.get_boxes(image, 0, 0)

        temp = image
        for i in range(len(boxes)):
            x1 = boxes[i].box_points[0][0]
            x2 = boxes[i].box_points[2][0]
            y1 = boxes[i].box_points[0][1]
            y2 = boxes[i].box_points[2][1]
            part = image[y1:y2, x1:x2]
            part = cv2.resize(part, (120, 32))
            part = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
            sign = TextRecognition.run_recognition(part, None, recognitor.run_vino_recognition)
            if not sign == "text":
                cv2.putText(temp, sign, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)
            cv2.rectangle(temp, (x1, y1), (x2, y2), (0, 0, 255), 2)
        image = temp

        temp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # TextRecognition.run_recognition(temp, None, recognitor.run_vino_recognition)

        if self.debug:
            cv2.imshow("img", image)
            cv2.waitKey()
        time = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S')
        log.info(time)
        file_name = "{}.jpg".format(time)

        result = cv2.imwrite(os.path.join(self.output_dir, file_name), image)
        log.info("Save result: {}".format(result))
        return "Image Uploaded Successfully"

    def run(self):
        output_dir = os.path.join("files")
        os.makedirs(output_dir, exist_ok=True)
        if os.path.exists(output_dir):
            self.output_dir = os.path.abspath(output_dir)
            log.info("Save directory created: {}".format(self.output_dir))
        self.app.run(host="0.0.0.0", port=self.port, threaded=True)


s = Server(5000)
s.run()
