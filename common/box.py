import numpy as np
import cv2
import re

from common.utils import DetectorUtils
import imutils


class Box(object):
    def __init__(self, box_points, bound_box, cnt, w, h, angle=0):
        # Add more if can
        self.bound_box_points = bound_box
        self.closest_number_box = None  # list of boxes with dist < max_dist / 2
        self.number_of_symbol = None  # len(text)
        self.angle = angle
        self.real_angle = 0
        self.check_list = {"VINO": False, "TESS": False, "BIN": False, "HAVE_MATCH": False}
        self.is_checked = False  # set when: False not in self.check_list.values()
        self.box_points = box_points  # minRect points,  Order: TL, TR, BR, BL
        self.box_point_moments = cv2.moments(box_points)
        self.counter = cnt  # source counter
        if self.box_point_moments['m00'] != 0:
            self.center = (int(self.box_point_moments['m10'] / self.box_point_moments['m00']),
                           int(self.box_point_moments['m01'] / self.box_point_moments['m00']))
        self.area = cv2.contourArea(cnt)
        self.text = {"VINO": "", "TESS": ""}
        self.H = h  # height of box
        self.W = w  # width of box
        # TODO list of number boxes
        self.list_of_inside_boxes = []  # update after binarization, contain Box
        self.class_of_text = {"text": False, "number": False, "num_text": False}
        self.closest_dists = []
        self.all_dists = []
        self.holst = None  # bin img after binarization
        self.temp_distanse = 0

    def cut_holst_from_bin_roi(self, holst, padding=0):
        nz = np.nonzero(holst)
        sh = holst.shape
        # cv2.imshow("holst", holst)
        # cv2.waitKey(1)
        minx = min(nz[0]) - padding
        minx = 0 if minx < 0 else minx
        maxx = max(nz[0]) + 1 + padding
        maxx = 0 if maxx > sh[0] else maxx
        miny = min(nz[1]) - padding
        miny = 0 if miny < 0 else miny
        maxy = max(nz[1]) + 1 + padding
        maxy = 0 if maxy > sh[1] else maxy
        self.holst = 255 - holst[minx:maxx, miny:maxy]

        return self.holst

    def plot_box(self, image):
        img_tmp = image.copy()
        cv2.drawContours(img_tmp, [self.box_points], 0, (50, 200, 50), 3)

        cv2.imshow('Detected text', imutils.resize(img_tmp, height=500))
        cv2.waitKey(1)

    @staticmethod
    def create_boxes_in_box_from_rects(box, rects, image):
        result = []
        for rect in rects:
            box_points = [[rect[0], rect[1] + rect[3]],
                          [rect[0], rect[1]],
                          [rect[0] + rect[2], rect[1]],
                          [rect[0] + rect[2], rect[1] + rect[3]]]
            box_points = np.int0(box_points)
            x, y, w, h = cv2.boundingRect(box_points)
            bound_box = np.asarray([[x, y], [x + w, y + h]])

            # cv2.imshow("image", cv2.drawContours(image, [box_points], -1, (255,0,0), -1))
            # cv2.waitKey()

            result.append(Box(DetectorUtils.order_points(box_points), bound_box, box_points, w, h))
        result.sort(key=lambda val: val.box_points[0][0], reverse=True)
        box.list_of_inside_boxes = result

    def get_text_by_recognizer(self, method):
        return self.text["VINO"] if "vino" in str(method) else self.text["TESS"]

    def set_text_by_recognizer(self, method, text):
        c = self.get_class_of_text(text)
        self.class_of_text[c] = True
        if "vino" in str(method):
            self.text["VINO"] = text
        else:
            self.text["TESS"] = text

    def set_vino_text(self, text):
        c = self.get_class_of_text(text)
        self.class_of_text[c] = True
        self.text["VINO"] = text

    @staticmethod
    def get_class_of_text(text):
        result = re.match(r"^[0-9]+$", text)  # онли текст
        if result is None:
            result = re.match(r"^[a-z]+$", text)
            if result is None:
                return "num_text"
            else:
                return "text"
        else:
            return "number"

    def set_tesseract_text(self, text):
        c = self.get_class_of_text(text)
        self.class_of_text[c] = True
        self.text["TESS"] = text

    def get_vino_text(self):
        return self.text["VINO"]

    def get_tesseract_text(self):
        return self.text["TESS"]

    def get_vino_check(self):
        return self.check_list["VINO"]

    def get_tesseract_check(self):
        return self.check_list["TESS"]

    def get_bin_text(self):
        return self.check_list["BIN"]

    def get_match_check(self):
        return self.check_list["HAVE_MATCH"]

    def set_vino_check(self):
        self.check_list["VINO"] = True

    def set_tesseract_check(self):
        self.check_list["TESS"] = True

    def set_bin_text(self):
        self.check_list["BIN"] = True

    def set_match_check(self):
        self.check_list["HAVE_MATCH"] = True

    def get_is_num_text(self):
        return self.class_of_text["num_text"]

    def get_is_number(self):
        return self.class_of_text["number"]

    def get_is_text(self):
        return self.class_of_text["text"]

    def set_is_num_text(self):
        for i in self.class_of_text:
            self.class_of_text[i] = False
        self.class_of_text["num_text"] = True

    def set_is_number(self):
        for i in self.class_of_text:
            self.class_of_text[i] = False
        self.class_of_text["number"] = True
