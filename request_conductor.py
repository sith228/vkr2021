import os
import time
import logging
import logging.config

import cv2
import time
import numpy as np
from flask import Flask, request, Response
from urllib.request import Request, urlopen


def init_logger():
    logger_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '%(message)s',
                'datefmt': '%d.%m %H:%M:%S',
            }, 'net': {
                'format': '%(message)s',
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
                'filename': "log/test_session_" + str(time.strftime("%Y-%m-%d %H-%M", time.gmtime())) + ".log",
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


def generate_image_table(path, table):
    for i in os.listdir(path):
        if i.endswith(".jpg") or i.endswith(".png") or i.endswith(".jpeg"):
            table.write(path + "|" + "\n")
        elif os.path.isdir(path + "/" + i):
            generate_image_table(path + "/" + i, table)


def start_test(path):
    table = open(path, 'r')
    right_answers = 0
    files_count = 0
    for line in table:
        files_count += 1
        line = line.split('|')
        image_path = line[0]
        image_label = line[1].rstrip('\n')
        image_answer = test_request(cv2.imread(image_path), "http://127.0.0.1:5000/save_image")
        image_answer = image_answer.decode("utf-8")
        if image_answer == image_label:
            log.debug("[RIGHT] Expected: %3s Received: %4s %s" % (image_label, image_answer, image_path))
            right_answers += 1
        else:
            log.debug("[WRONG] Expected: %3s Received: %4s %s" % (image_label, image_answer, image_path))
    log.debug("Right: %d, All: %d, Accuracy: %f" % (right_answers, files_count, right_answers / files_count))
    table.close()


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

    return r
    # Decoding answer
    start_time = time.time()
    image = np.frombuffer(r, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print((time.time() - start_time) * 1e+3, " Decoding answer time ")

    # Show results
    # print("image shape ", image.shape)
    # cv2.imshow("img ", image)
    cv2.waitKey(1)
    print("done")


init_logger()
log = logging.getLogger("root")


# Generate table template
# table = open("test/table.txt", 'w')
# generate_image_table("test", table)
# table.close()


start_test("test/table.txt")
