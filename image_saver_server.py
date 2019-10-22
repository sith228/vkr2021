import os
from datetime import datetime

import cv2
import time
import numpy as np
from flask import Flask, request, Response
from urllib.request import Request, urlopen
import logging
import logging.config


def test_request(img, url):
    """
    Send jpg image to url in http post request
    :param img: numpy array of image
    :param url: url to send img
    :return: nothing
    """

    print("image shape", img.shape)
    # Encoding data
    start_time = time.time()
    data = (cv2.imencode(".jpg", img)[1].tobytes())
    print((time.time() - start_time) * 1e+3, " Prepare http request time ")

    # Prepare http request
    start_time = time.time()
    headers = {'content-type': 'image/jpeg'}
    print(len(data))
    req = Request(url, data=data, headers=headers)
    print((time.time() - start_time) * 1e+3, " Prepare http request time ")

    # Send
    start_time = time.time()
    r = urlopen(req).read()
    print((time.time() - start_time) * 1e+3, " Send time ")

    # Decoding answer
    start_time = time.time()
    image = np.frombuffer(r, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print((time.time() - start_time) * 1e+3, " Decoding answer time ")

    # Show results
    print("image shape ", image.shape)
    cv2.imshow("img ", image)
    cv2.waitKey(1)


# Local Url
url = "http://127.0.0.1:5000/save_image"
# Photo location
image_path = "semantic-segmentation-adas-0001\\16_berlin_io.jpg"
# Read photo
photo = cv2.imread(image_path)
# Test POST http request
test_request(photo, url=url)


# def test_request(img, url="http://127.0.0.1:5000/save_image"):
#     '''
#     Send jpg image to url in http post request
#     :param img: numpy array of image
#     :param url: url
#     :return: nothing
#     '''
#     headers = {'content-type': 'image/jpeg'}
#     req = request.Request(url, data=img, headers=headers)
#     request.urlopen(req)


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
