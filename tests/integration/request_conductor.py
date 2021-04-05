import os
import time
import logging
import logging.config
import configparser
import argparse

import cv2
import time
import numpy as np
from flask import Flask, request, Response
from urllib.request import Request, urlopen


def init_arg_parser():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("-ip", default="127.0.0.1:5000", type=str, action="store", help="Server IP")

    return parser

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


def init_config(config_path, images_path):
    config = configparser.ConfigParser()
    config.add_section("Labels")
    config = add_images(config, images_path)
    with open(config_path, "w") as config_file:
        config.write(config_file)


def add_images(config, path):
    for i in os.listdir(path):
        if i.endswith(".jpg") or i.endswith(".png") or i.endswith(".jpeg"):
            config.set("Labels", path + '/' + i, "")
        elif os.path.isdir(path + '/' + i):
            config = add_images(config, path + '/' + i)
    return config


def start_test(config, args):
    right_answers = 0
    files_count = 0
    images = config.options("Labels")
    start_time = time.time()
    for image in images:
        files_count += 1
        if not os.path.isfile(image):
            log.debug("[ERROR] Can't find file %s" % image)
            continue
        image_label = config.get("Labels", image)
        image_time_start = time.time()
        image_answer = test_request(cv2.imread(image), "http://" + args.ip + "/load_low_res_image")
        image_answer = image_answer.decode("utf-8")
        image_time_end = time.time()
        if image_answer == image_label:
            log.debug("[RIGHT] Time: %1.3f Expected: %3s Received: %4s %s" % (image_time_end - image_time_start, image_label, image_answer, image))
            right_answers += 1
        else:
            log.debug("[WRONG] Time: %1.3f Expected: %3s Received: %4s %s" % (image_time_end - image_time_start, image_label, image_answer, image))
    end_time = time.time()
    log.debug("Right: %d, All: %d, Accuracy: %f, Time: %f" % (right_answers, files_count, right_answers / files_count, end_time - start_time))


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

arg_parser = init_arg_parser()
args = arg_parser.parse_args()

if not os.path.exists("../../test/config.cfg"):
    init_config("../../test/config.cfg", ".")
config = configparser.ConfigParser()
config.read("config.cfg")

start_test(config, args)

