import argparse
import os
import sys
import time
import imutils

import cv2
import numpy as np

from common.utils import DetectorUtils
from common.utils import InferenceEngine
from common.utils import OpenCvInference
from common.box import Box


class PixelLinkDecoder(DetectorUtils):
    def __init__(self, image, pixel_scores, link_scores,
                 pixel_conf_threshold, link_conf_threshold, four_neighbours=False):
        # print(pixel_scores.shape) # 1. 2. 96. 96.
        # print(link_scores.shape) # 1. 16. 96. 96.
        self.image_shape = image.shape[0:2]
        self.pixel_scores = self._set_pixel_scores(pixel_scores)
        self.link_scores = self._set_link_scores(link_scores)

        if four_neighbours:
            self._get_neighbours = self._get_neighbours_4
        else:
            self._get_neighbours = self._get_neighbours_8

        self.pixel_conf_threshold = pixel_conf_threshold
        self.link_conf_threshold = link_conf_threshold
        self.pixel_mask = self.pixel_scores >= self.pixel_conf_threshold
        self.link_mask = self.link_scores >= self.link_conf_threshold
        self.points = list(zip(*np.where(self.pixel_mask)))
        self.h, self.w = np.shape(self.pixel_mask)
        self.group_mask = dict.fromkeys(self.points, -1)
        self.bboxes = None
        self.root_map = None
        self.mask = None

    def _softmax(self, x, axis=None):
        return np.exp(x - self._logsumexp(x, axis=axis, keepdims=True))

    @staticmethod
    def _logsumexp(a, axis=None, b=None, keepdims=False, return_sign=False):
        if b is not None:
            a, b = np.broadcast_arrays(a, b)
            if np.any(b == 0):
                a = a + 0.  # promote to at least float
                a[b == 0] = -np.inf

        a_max = np.amax(a, axis=axis, keepdims=True)

        if a_max.ndim > 0:
            a_max[~np.isfinite(a_max)] = 0
        elif not np.isfinite(a_max):
            a_max = 0

        if b is not None:
            b = np.asarray(b)
            tmp = b * np.exp(a - a_max)
        else:
            tmp = np.exp(a - a_max)

        # suppress warnings about log of zero
        with np.errstate(divide='ignore'):
            s = np.sum(tmp, axis=axis, keepdims=keepdims)
            if return_sign:
                sgn = np.sign(s)
                s *= sgn  # /= makes more sense but we need zero -> zero
            out = np.log(s)

        if not keepdims:
            a_max = np.squeeze(a_max, axis=axis)
        out += a_max

        if return_sign:
            return out, sgn
        else:
            return out

    def _set_pixel_scores(self, pixel_scores):
        "get softmaxed properly shaped pixel scores"
        tmp = np.transpose(pixel_scores, (0, 2, 3, 1))
        return self._softmax(tmp, axis=-1)[0, :, :, 1]

    def _set_link_scores(self, link_scores):
	
        "get softmaxed properly shaped links scores"
        tmp = np.transpose(link_scores, (0, 2, 3, 1))
        tmp_reshaped = tmp.reshape(tmp.shape[:-1] + (8, 2))
        return self._softmax(tmp_reshaped, axis=-1)[0, :, :, :, 1]

    def _find_root(self, point):
        root = point
        update_parent = False
        tmp = self.group_mask[root]
        while tmp is not -1:
            root = tmp
            tmp = self.group_mask[root]
            update_parent = True
        if update_parent:
            self.group_mask[point] = root
        return root

    def _join(self, p1, p2):
        root1 = self._find_root(p1)
        root2 = self._find_root(p2)
        if root1 != root2:
            self.group_mask[root2] = root1

    def _get_index(self, root):
        if root not in self.root_map:
            self.root_map[root] = len(self.root_map) + 1
        return self.root_map[root]

    def _get_all(self):
        self.root_map = {}
        self.mask = np.zeros_like(self.pixel_mask, dtype=np.int32)

        for point in self.points:
            point_root = self._find_root(point)
            bbox_idx = self._get_index(point_root)
            self.mask[point] = bbox_idx

    def _get_neighbours_8(self, x, y):
        w, h = self.w, self.h
        tmp = [(0, x - 1, y - 1), (1, x, y - 1),
               (2, x + 1, y - 1), (3, x - 1, y),
               (4, x + 1, y), (5, x - 1, y + 1),
               (6, x, y + 1), (7, x + 1, y + 1)]

        return [i for i in tmp if i[1] >= 0 and i[1] < w and i[2] >= 0 and i[2] < h]

    def _get_neighbours_4(self, x, y):
        w, h = self.w, self.h
        tmp = [(1, x, y - 1),
               (3, x - 1, y),
               (4, x + 1, y),
               (6, x, y + 1)]

        return [i for i in tmp if i[1] >= 0 and i[1] < w and i[2] >= 0 and i[2] < h]

    def mask_to_boxes(self, min_area, min_height):
        image_h, image_w = self.image_shape
        self.bboxes = []
        max_bbox_idx = self.mask.max()
        mask_tmp = cv2.resize(self.mask, (image_w, image_h), interpolation=cv2.INTER_NEAREST)

        for bbox_idx in range(1, max_bbox_idx + 1):
            bbox_mask = mask_tmp == bbox_idx
            cnts, _ = cv2.findContours(bbox_mask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) == 0:
                continue
            cnt = cnts[0]
            rect, w, h, angle = self.min_area_rect(cnt)
            if min(w, h) < min_height:
                continue
            if w * h < min_area:
                continue
            bound_box, w, h = self.get_bound_box(cnt)
            self.bboxes.append(Box(self.order_points(rect), bound_box, cnt, w, h, angle))
        return self.bboxes

    def decode(self):
        for point in self.points:
            y, x = point
            neighbours = self._get_neighbours(x, y)
            for n_idx, nx, ny in neighbours:
                link_value = self.link_mask[y, x, n_idx]
                pixel_cls = self.pixel_mask[ny, nx]
                if link_value and pixel_cls:
                    self._join(point, (ny, nx))

        self._get_all()

    def plot_result(self, image):
        img_tmp = image.copy()
        self.bboxes.sort(key=lambda x: x.H, reverse=True)  # sort box by rect area
        for box in self.bboxes:
            cv2.drawContours(img_tmp, [box.box_points], 0, (50, 200, 50), 3)

        #cv2.imshow('Detected text', cv2.resize(img_tmp, (640, 480)))
        cv2.imshow('Detected text', imutils.resize(img_tmp, height=500))
        cv2.waitKey(1)
        # cv2.destroyAllWindows()
        # if cv2.waitKey():
        #     cv2.destroyAllWindows()


class OVTextDetector(object):
    # load models
    def __init__(self, ie=True):
        print("Load text-detection-0002.xml")

        model_xml = os.path.join("tools", "models", "openvino_text_detection", "text-detection-0002.xml")
        model_bin = os.path.join("tools", "models", "openvino_text_detection", "text-detection-0002.bin")

        print(os.path.exists(model_bin))
        print(os.path.exists(model_xml))

        self.w = 768
        self.h = 768
        self.debug2 = False

        if not ie:
            self.opencv = OpenCvInference(model_xml, model_bin, self.w, self.h)
            self.inference = self.opencv.inference_sync
        else:
            self.ie = InferenceEngine(model_xml, model_bin, self.w, self.h)
            self.inference = self.ie.inference_sync

        self.td_net = cv2.dnn.readNet(model_xml, model_bin)

    # run detector on image
    def get_boxes(self, image, min_area, min_height):
        start_time = time.time()
        pixel_scores, link_scores = self.inference(cv2.resize(image, (self.h, self.w)))
        print((time.time() - start_time)*1e+3, " text-detection-0002 runtime")

        dcd = PixelLinkDecoder(image, pixel_scores, link_scores,
                               pixel_conf_threshold=0.8, link_conf_threshold=0.8)
        dcd.decode()
        boxes = dcd.mask_to_boxes(min_area, min_height)
        if self.debug2:
            dcd.plot_result(image.copy())
        return boxes


def main():
    from tools.models.openvino_text_recognition.text_recognition import OVTextRecognition

    def parse_args():
        ap = argparse.ArgumentParser()
        # ap.add_argument("-i", required=True, dest="image_path", help="path to input image")
        ap.add_argument("-m", required=True, dest="model_path", help="path to model's XML file")
        ap.add_argument("-mr", required=True, dest="recogn_path", help="path to model's XML file")
        args = ap.parse_args()
        return args

    # args = parse_args()
    # if args.model_path.endswith('.xml'):
    #     # img = cv2.imread(args.image_path)
    #     td = cv2.dnn.readNet(args.model_path, args.model_path[:-3] + 'bin')
    # else:
    #     print("Not valid model's XML file name (should be something liike 'foo.xml')")
    #     sys.exit()
    text_recognition = OVTextRecognition()
    text_detection = OVTextDetector()
    cap = cv2.VideoCapture(0)
    while cv2.waitKey(1) < 0:
        startrTime = time.time()
        has_frame, img = cap.read()
        if not has_frame:
            break
        boxes = text_detection.get_boxes(img, min_area=100, min_height=10)
        if False:
            text_recognition.run_recognition_holst_boxes(boxes,
                                                         text_recognition.run_vino_recognition)
        print("detection time "+str((time.time() - startrTime)*1e+3))
        # blob = cv2.dnn.blobFromImage(img, 1, (384, 384), ddepth=cv2.CV_8U)
        # td.setInput(blob)
        # a, b = td.forward(td.getUnconnectedOutLayersNames())
        # dcd = PixelLinkDecoder(img, a, b,)
        # dcd.decode()  # results are in dcd.bboxes
        # dcd.plot_result(img)


if __name__ == '__main__':
    sys.exit(main() or 0)
