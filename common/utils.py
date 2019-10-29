from urllib.request import urlopen
from openvino.inference_engine import IENetwork, IEPlugin

import numpy as np
import platform
import imutils
import time
import cv2
import sys
import os

import requests


def download_image(pic_url):
    response = requests.get(pic_url, stream=True)
    if not response.ok:
        print("Download image", response)

    req = urlopen(pic_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def resize_to_show(img, width=300):
    s = img.shape[:2]; asp_rat = s[0] / s[1]; height = int(width * asp_rat)
    return cv2.resize(img, (width, height))


def show_image(img, name="Debug", pause=1, width=300):
    cv2.imshow(name, resize_to_show(img, width))
    cv2.waitKey(pause)


class OsUtil(object):
    @staticmethod
    def is_windows():
        return platform.system().lower() == "windows"

    @staticmethod
    def is_macos():
        return platform.system().lower() == "darwin"

    @staticmethod
    def is_linux():
        return platform.system().lower() == "linux"


class DetectorUtils(object):
    @staticmethod
    def min_area_rect(cnt):
        rect = cv2.minAreaRect(cnt)
        w, h = rect[1]
        angle = rect[-1]
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        return box, w, h, angle

    @staticmethod
    def get_bound_box(cnt):
        x, y, w, h = cv2.boundingRect(cnt)
        return np.asarray([[x, y], [x + w, y + h]]), w, h

    @staticmethod
    def order_points(rect):
        """ (x, y)
            Order: TL, TR, BR, BL
        """
        tmp = np.zeros_like(rect)
        sums = rect.sum(axis=1)
        tmp[0] = rect[np.argmin(sums)]
        tmp[2] = rect[np.argmax(sums)]
        diff = np.diff(rect, axis=1)
        tmp[1] = rect[np.argmin(diff)]
        tmp[3] = rect[np.argmax(diff)]
        return tmp


# correct solution:
def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0) # only difference


class RecognitionUtils(object):
    def __init__(self):
        self.augment_num = cv2.imread(os.path.join('common', 'augmentation_images', '6.png'), 0)
        self.augment_num2 = cv2.imread(os.path.join('common', 'augmentation_images', '2.png'), 0)

    @staticmethod
    def resize_for_open_vino(image):
        image = imutils.resize(image, height=32)
        # image = image_resize(image, height=32)
        if image.shape[1] > 120:
            return cv2.resize(image, (120, 32))

        padd_left = (120 - image.shape[1]) // 2
        padd_right = 120 - padd_left - image.shape[1]

        image = cv2.copyMakeBorder(image, 0, 0, padd_left, padd_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        #cv2.imwrite("{}.jpeg".format(time.time()), image)
        # cv2.imshow("rsize_for_vino", image)
        # cv2.waitKey(1)

        return image

    @staticmethod
    def decode_sequence(prob):
            symbols = '0123456789abcdefghijklmnopqrstuvwxyz '
            sequence = ''
            seq_p = []
            prev_pad = False
            for pos in prob.reshape(30, 37):
                s = softmax(pos)
                idx = np.argmax(pos)
                symbol = symbols[idx]
                if symbol != ' ':
                    if sequence == '' or prev_pad or (sequence != '' and symbol != sequence[-1]):
                        prev_pad = False
                        sequence += symbols[idx]
                        seq_p.append(s[idx])
                else:
                    prev_pad = True
            return sequence, seq_p

    def augment_data(self, image, components_count):  # use for components_count 1 or 2
        _, augment_num1 = cv2.threshold(self.augment_num, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if components_count == 1:
            image = cv2.resize(image, (38, 28))
            image = np.concatenate((image, self.augment_num), axis=1)
            image = np.concatenate((image, self.augment_num), axis=1)
        if components_count == 2:
            image = cv2.resize(image, (76, 28))
            image = np.concatenate((image, self.augment_num), axis=1)
        return self.add_padding_for_open_vino(image)

    def alter_augment_data(self, image, components_count):  # use for components_count 1 or 2
        _, augment_num1 = cv2.threshold(self.augment_num2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if components_count == 1:
            image = cv2.resize(image, (38, 28))
            image = np.concatenate((image, self.augment_num2), axis=1)
            image = np.concatenate((image, self.augment_num2), axis=1)
        if components_count == 2:
            image = cv2.resize(image, (76, 28))
            image = np.concatenate((image, self.augment_num2), axis=1)
        return self.add_padding_for_open_vino(image)

    @staticmethod
    def add_padding_for_open_vino(image):  # 114x28 to 120x32
        image = cv2.copyMakeBorder(image, 2, 2, 3, 3, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        return image


class BinarizaionUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def resize_for_open_vino(image):
        image = imutils.resize(image, height=32)
        # image = image_resize(image, height=32)
        if image.shape[1] > 120:
            return cv2.resize(image, (120, 32))

        padd_left = (120 - image.shape[1]) // 2
        padd_right = 120 - padd_left - image.shape[1]

        image = cv2.copyMakeBorder(image, 0, 0, padd_left, padd_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        #cv2.imwrite("{}.jpeg".format(time.time()), image)
        # cv2.imshow("rsize_for_vino", image)
        # cv2.waitKey(1)

        return image

    @staticmethod
    def is_point_in_rect(point, rect):

        if point[0] > rect[0] and point[1] > rect[1]:
            if point[0] < rect[0] + rect[2] and point[1] < rect[1] + rect[3]:
                return True
        return False

    @staticmethod
    def orientate(image):
        bin = image
        # транспонирование изображения
        flipped = cv2.flip(bin, 1)
        (h, w) = flipped.shape[:2]
        center = (w / 2, w / 2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        transpose = cv2.warpAffine(flipped, M, (h, w))

        coords = np.column_stack(np.where(transpose > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)

        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle
        return angle, BinarizaionUtils.rotate_img(image, angle)

    @staticmethod
    def rotate_img(image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, -angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 borderMode=cv2.BORDER_REPLICATE)
        return rotated


class InferenceEngine(object):
    def __init__(self, xml, bin, c_w=0, c_h=0, device="CPU", cpu_extension=""):
        print('Loading IR to the plugin...')
        self.model_xml = xml
        self.model_bin = bin
        self.device = device
        if cpu_extension == "":
            extension_folder = os.path.abspath(os.path.join("tools", "InferenceEngine"))
            if OsUtil.is_windows():
                # C:\Users\Igor\work\access_city\cloud-bus-recognition\tools\InferenceEngine\cpu_extension.dll
                self.cpu_extension = os.path.join(extension_folder, "cpu_extension.dll")
                if not os.listdir(extension_folder):
                    # "IntelSWTools\openvino\inference_engine\bin\intel64\Release"
                    self.cpu_extension = os.path.join("\\Program Files (x86)\\IntelSWTools\\openvino",
                                                      "inference_engine\\bin\\intel64\\Release",
                                                      "cpu_extension.dll")
            elif OsUtil.is_macos():
                self.cpu_extension = os.path.join(extension_folder, "libcpu_extension.dylib")
                if not os.listdir(extension_folder):
                    self.cpu_extension = os.path.join("/opt/intel/openvino/inference_engine/lib/intel64",
                                                      "libcpu_extension.dylib")
            else:
                self.cpu_extension = os.path.join(extension_folder, "libcpu_extension.so")
                if not os.listdir(extension_folder):
                    self.cpu_extension = os.path.join("/opt/intel/openvino/inference_engine/lib/intel64/Release",
                                                      "libcpu_extension_avx2.so")
        else:
            self.cpu_extension = cpu_extension
        self.plugin = IEPlugin(device=device, plugin_dirs="")
        if self.cpu_extension and 'CPU' in self.device:
            if os.path.exists(self.cpu_extension):
                self.plugin.add_cpu_extension(self.cpu_extension)
            else:
                print("Warning: CPU EXTENSION NOT FOUND")
        self.net = IENetwork(model=xml, weights=bin)

        if c_w != 0 or c_h != 0:
            inputs = self.net.inputs
            n, c, h, w = self.net.inputs['Placeholder'].shape
            inputs['Placeholder'] = (n, c, c_h, c_w)
            self.net.reshape(inputs)

        self.exec_net = self.plugin.load(network=self.net, num_requests=2)

    # DON'T WORK CORRECT
    @staticmethod
    def check_layers_support(net, plugin):
        if plugin.device == 'CPU':
            supported_layers = plugin.get_supported_layers(net)
            not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
            if len(not_supported_layers) != 0:
                print('Following layers are not supported by the plugin for specified device {}:\n\t{}'.
                      format(plugin.device,
                             '\n\t'.join('{} ({} with params {})'.format(layer_id, net.layers[layer_id].type,
                                                                         str(net.layers[layer_id].params))
                                         for layer_id in not_supported_layers)
                             )
                      )
                print(
                    "Please try to specify cpu extensions library in "
                    "'tools/InferenceEngine/cpu_extension.dll'")
                sys.exit(1)

    def inference_sync(self, frame):
        # input_image = frame
        print('Starting inference...')
        if len(frame.shape) == 3:
            frame = frame.transpose((2, 0, 1))
        # else:
        #     input_image = input_image.transpose(0, 1))
        n, c, h, w = self.net.inputs['Placeholder'].shape
        frame = frame.reshape((n, c, h, w)).astype(np.float32)

        # Run the net.
        outputs = self.exec_net.infer({'Placeholder': frame})
        if len(self.net.outputs.keys()) > 1:
            result = [outputs[k] for k in self.net.outputs.keys()]
            result.sort(key=lambda x: x.shape[1])
            return result
        return outputs[next(iter(self.net.outputs.keys()))]


class OpenCvInference(object):
    def __init__(self, xml, bin, w, h):
        self.td_net = cv2.dnn.readNet(xml, bin)
        self.h = h
        self.w = w

    def inference_sync(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1, (self.h, self.w), ddepth=cv2.CV_8U)
        self.td_net.setInput(blob)
        out = self.td_net.forward(self.td_net.getUnconnectedOutLayersNames())
        return out
