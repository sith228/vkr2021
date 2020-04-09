import os
import time

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

import cv2
from common import craft_utils
from common import imgproc
from common import file_utils

from tools.models.craft_text_segmentation.craft import CRAFT

from collections import OrderedDict


def copy_state_dict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict


class CraftTextDetector(object):
    trained_model = 'weights/craft_mlt_25k.pth'
    text_threshold = 0.7
    low_text = 0.5
    link_threshold = 0.0
    cuda = False
    canvas_size = 1280
    mag_ratio = 1.5
    poly = False
    show_time = False

    # load models
    def __init__(self, cuda=False):
        print("Load text-detection-0002.xml")
        dirname = os.getcwd()
        if os.path.basename(dirname) != "text_detection":
            trained_model = os.path.join("tools", "text_detection", "craft_mlt_25k.pth")
        else:
            trained_model = os.path.join("craft_mlt_25k.pth")

        print(os.path.exists(trained_model))

        self.w = 1280
        self.h = 768

        # load net
        self.net = CRAFT()     # initialize

        print('Loading weights from checkpoint (' + trained_model + ')')
        if cuda:
            self.net.load_state_dict(copy_state_dict(torch.load(trained_model)))
        else:
            self.net.load_state_dict(copy_state_dict(torch.load(trained_model, map_location='cpu')))

        if cuda:
            self.net = self.net.cuda()
            self.net = torch.nn.DataParallel(self.net)
            cudnn.benchmark = False
        self.net.eval()

    # pre-processing
    def preproc(self, image):
        # resize
        img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, CraftTextDetector.canvas_size,
                                                                              interpolation=cv2.INTER_LINEAR,
                                                                              mag_ratio=CraftTextDetector.mag_ratio)
        ratio_h = ratio_w = 1 / target_ratio
        # preprocessing
        x = imgproc.normalizeMeanVariance(img_resized)
        x = torch.from_numpy(x).permute(2, 0, 1)  # [h, w, c] to [c, h, w]
        x = Variable(x.unsqueeze(0))  # [c, h, w] to [b, c, h, w]
        return img_resized, target_ratio, size_heatmap, x, ratio_h, ratio_w

    # run detector on image
    def test_net(self, image, text_threshold, link_threshold, low_text, poly):
        t0 = time.time()

        img_resized, target_ratio, size_heatmap, x, ratio_h, ratio_w = self.preproc(image)

        if self.cuda:
            x = x.cuda()
        # forward pass
        y, _ = self.net(x)

        # make score and link map
        score_text = y[0, :, :, 0].cpu().data.numpy()
        score_link = y[0, :, :, 1].cpu().data.numpy()

        t0 = time.time() - t0
        t1 = time.time()
        # Post-processing
        boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold,
                                               link_threshold, low_text, poly, image)
        boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
        polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)

        for k in range(len(polys)):
            if polys[k] is None:
                polys[k] = boxes[k]

        t1 = time.time() - t1

        # render results (optional)
        ret_score_text = self.postproc(score_text)

        # if args.show_time:
        print("\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

        return boxes, polys, ret_score_text

    def postproc(self, score_text):
        render_img = score_text.copy()
        ret_score_text = imgproc.cvt2HeatmapImg(render_img)
        cv2.imshow("render_img", render_img)
        cv2.waitKey(1)
        return ret_score_text

    def get_boxes(self, image):
        return self.test_net(image,
                             CraftTextDetector.text_threshold,
                             CraftTextDetector.link_threshold,
                             CraftTextDetector.low_text,
                             CraftTextDetector.poly)


def main():
    """ For test images in a folder """
    Datasets_folder = "C:\\Users\\Igor\\work\\prices\\price-recognition\\Datasets\\temp_dataset"
    image_list = [os.path.join(Datasets_folder, i) for i in os.listdir(Datasets_folder)]

    result_folder = './result/'
    if not os.path.isdir(result_folder):
        os.mkdir(result_folder)
    # load net
    detector = CraftTextDetector()

    t = time.time()
    print("Data load")
    # load data
    for k, image_path in enumerate(image_list):
        print("Test image {}/{}: {}".format(k+1, len(image_list), image_path))
        image = imgproc.loadImage(image_path)

        bboxes, polys, score_text = detector.get_boxes(image)

        # save score text
        filename, file_ext = os.path.splitext(os.path.basename(image_path))
        mask_file = result_folder + "/res_" + filename + '_mask.jpg'
        cv2.imshow("score_text", score_text)
        cv2.waitKey(1)
        cv2.imwrite(mask_file, score_text)

        file_utils.saveResult(image_path, image[:,:,::-1], polys, dirname=result_folder)

    print("elapsed time : {}s".format(time.time() - t))


if __name__ == '__main__':
    main()
