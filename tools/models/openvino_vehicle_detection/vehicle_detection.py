from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import time
import logging as log

from openvino.inference_engine import IENetwork, IECore


def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument("-m", "--model", help="Required. Path to an .xml file with a trained model.",
                      required=True, type=str)
    args.add_argument("-i", "--input",
                      help="Required. Path to video file or image. 'cam' for capturing video stream from camera",
                      required=True, type=str)
    args.add_argument("-l", "--cpu_extension",
                      help="Optional. Required for CPU custom layers. Absolute path to a shared library with the "
                           "kernels implementations.", type=str, default=None)
    args.add_argument("-d", "--device",
                      help="Optional. Specify the target device to infer on; CPU, GPU, FPGA, HDDL or MYRIAD is "
                           "acceptable. The demo will look for a suitable plugin for device specified. "
                           "Default value is CPU", default="CPU", type=str)
    args.add_argument("--labels", help="Optional. Path to labels mapping file", default=None, type=str)
    args.add_argument("-pt", "--prob_threshold", help="Optional. Probability threshold for detections filtering",
                      default=0.5, type=float)
    args.add_argument("--no_show", help="Optional. Don't show output", action='store_true')

    return parser

class OVVehicleDetector():
    def __init__(self):
        model_xml = os.path.join("tools", "models", "openvino_vehicle_detection", "vehicle-detection-adas-0002.xml")
        model_bin = os.path.join("tools", "models", "openvino_vehicle_detection", "vehicle-detection-adas-0002.bin")
        #Place for your CPU extensions
        #ie.add_extension(args.cpu_extension, "CPU"
        self.net = IENetwork(model=model_xml, weights=model_bin)
        self.ie = IECore()

        img_info_input_blob = None
        self.feed_dict = {}
        for blob_name in self.net.inputs:
            if len(self.net.inputs[blob_name].shape) == 4:
                self.input_blob = blob_name
            elif len(self.net.inputs[blob_name].shape) == 2:
                img_info_input_blob = blob_name
            else:
                raise RuntimeError("Unsupported {}D input layer '{}'. Only 2D and 4D input layers are supported"
                                   .format(len(self.net.inputs[blob_name].shape), blob_name))

        assert len(self.net.outputs) == 1, "Demo supports only single output topologies"

        self.out_blob = next(iter(self.net.outputs))
        log.info("Loading IR to the plugin...")
        self.exec_net = self.ie.load_network(network=self.net, num_requests=2, device_name="CPU")
        self.n, self.c, self.h, self.w = self.net.inputs[self.input_blob].shape
        if img_info_input_blob:
            self.feed_dict[img_info_input_blob] = [h, w, 1]

    def get_boxes(self, image):

        labels_map = None

        # Starting
        frame_h, frame_w = image.shape[:2]
        image_copy = image.copy()
        image = cv2.resize(image, (self.w, self.h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        image = image.reshape((self.n, self.c, self.h, self.w))
        self.feed_dict[self.input_blob] = image
        self.exec_net.start_async(request_id=0, inputs=self.feed_dict)

        # Parse detection results of the current request
        self.exec_net.requests[0].wait(-1)
        res = self.exec_net.requests[0].outputs[self.out_blob]
        for obj in res[0][0]:
            # Draw only objects when probability more than specified threshold
            if obj[2] > 0.5: #THRESOLD!!!
                xmin = int(obj[3] * frame_w)
                ymin = int(obj[4] * frame_h)
                xmax = int(obj[5] * frame_w)
                ymax = int(obj[6] * frame_h)
                class_id = int(obj[1])
                # Draw box and label\class_id
                color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
                cv2.rectangle(image_copy, (xmin, ymin), (xmax, ymax), color, 2)
                det_label = labels_map[class_id] if labels_map else str(class_id)
                cv2.putText(image_copy, det_label + ' ' + str(round(obj[2] * 100, 1)) + ' %', (xmin, ymin - 7),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)

        cv2.imshow("Detection Results", image_copy)
        cv2.waitKey()