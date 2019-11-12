import os
import time

import cv2
import time
import numpy as np
from flask import Flask, request, Response
from urllib.request import Request, urlopen


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

def generate_image_table(path, table):
    for i in os.listdir(path):
        if i.endswith(".jpg") or i.endswith(".png") or i.endswith(".jpeg"):
            table.write("\"" + path + "/" + i + "\"" + "\n")
        elif os.path.isdir(path + "/" + i):
            generate_image_table(path + "/" + i, table)


def start_test(path):
    table = open(path, 'r')
    log_file = open("log/test_session_" + str(time.strftime("%Y-%m-%d %H-%M", time.gmtime())) + ".log", 'w')
    right_answers = 0
    files_count = 0
    for line in table:
        files_count += 1
        image_path = line[1: line.find("\"", 1)]
        image_label = line[line.find("\" ") + 2 : len(line) - 1]
        image_answer = test_request(cv2.imread(image_path), "http://127.0.0.1:5000/save_image")
        image_answer = image_answer.decode("utf-8")
        if image_answer == image_label:
            log_file.write("[SUCCESS] ")
            right_answers += 1
        else:
            log_file.write("[FAILED] ")
        log_file.write(image_path + " Expected: " + image_label + " Recieved " + str(image_answer) + "\n")
    log_file.write("Files: %d   Right: %d   Accuracy: %d" % (files_count, right_answers, right_answers / files_count))
    log_file.close()
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


# Local Url
url = "http://127.0.0.1:5000/save_image"
# Photo location
image_path = "test/IMG_20191024_142434.jpg"
# "testImage.jpg"
# Read photo
photo = cv2.imread(image_path)
# Test POST http request
# test_request(photo, url=url)

# Generate table template
# table = open("test/table.txt", 'w')
# generate_image_table("test", table)
# table.close()


start_test("test/table.txt")
