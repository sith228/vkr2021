
import cv2
import traceback
import numpy as np

from common.Box import Box
from common.utils import show_image
from common.utils import BinarizaionUtils


class Binarizaion(BinarizaionUtils):
    def __init__(self, debug=False):
        super().__init__()

        self.debug_mode = debug
        self.debug2 = False
        pass

    def get_splited_boxes_by_number(self, image, boxes, force=False):
        _count = 1
        for box in boxes:
            _count = _count+1
            if not force:
                if box.get_bin_text():
                    continue
            try:
                roi, start_roi, padding = self.get_big_roi(image, box)
                if self.debug2:
                    box.plot_box(image)
                if self.debug_mode:
                    show_image(roi, "roi")
                #cv2.imwrite("logs\\roi\\{}.jpeg".format(time.time()), roi)

                #find otsu tresh in small rect
                im_gray = cv2.GaussianBlur(cv2.cvtColor(self.get_small_roi(image, box), cv2.COLOR_RGB2GRAY), (3, 3), 0)
                tresh = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]

                im_gray = cv2.GaussianBlur(cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY), (3, 3), 0)
                # _, th = cv2.threshold(im_gray, tresh, 255, cv2.THRESH_BINARY)
                th = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 6)

                th = cv2.bitwise_not(th)

                contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if self.debug_mode:
                    show_image(th, "roi")
                full_counters = self.find_best_counters(roi, contours, padding)
                angle, holst = self.create_holst_from_counters(roi, box, full_counters)
                rects = self.get_rects_from_holst(full_counters, holst.shape, roi.shape)
                box.rects_inside = [(start_roi[0] + rect[0] - 5, start_roi[1] + rect[1] - 5,
                                     rect[2] + 10, rect[3] + 10) for rect in rects]
                Box.create_boxes_in_box_from_rects(box, box.rects_inside, image)
                box.real_angle = angle
                box.set_bin_text()
                if self.debug_mode:
                    cv2.imshow("box.holst", box.holst)
                    cv2.waitKey(0)
                try:
                    if self.debug_mode:
                        #box.plot_box(image)
                        print("======================================")
                        print("DEBUG BINARIZATION")
                        print("======================================")
                        print(roi.shape)
                        print("======================================")
                        print(rects)
                        print("======================================")
                        print("END DEBUG")
                        print("======================================")
                        i = roi.copy()
                        for rect in rects:
                            cv2.rectangle(i, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 4)

                        show_image(i, "draw rects on big roi", width=640)

                except Exception as e:
                    # traceback.print_exc()
                    print("Exception:", e)
            except Exception as e:
                print("Exception:", e)
                # traceback.print_exc()
                # box.plot_box(image)
        return boxes

    @staticmethod
    def get_big_roi(image, box):
        r_x = box.W
        r_y = box.H
        left_padd = 0
        right_padd = 0
        top_padd = 0
        bottom_padd = 0
        start_roi = (int(box.center[0] - r_x), int(box.center[1] - r_y))
        rect = [start_roi[0], int(box.center[0] + r_x),
                start_roi[1], int(box.center[1] + r_y)]

        if 0 > rect[0]:
            left_padd = -rect[0]
            rect[0] = 0
        else:
            rect[0]
        if 0 > rect[2]:
            top_padd = -rect[2]
            rect[2] = 0
        else:
            rect[2]
        if rect[1] > image.shape[1]:
            right_padd = rect[1]-image.shape[1]
            rect[1] = image.shape[1]
        else:
            rect[1]
        if rect[3] > image.shape[0]:
            bottom_padd = rect[3]-image.shape[0]
            rect[3] = image.shape[0]
        else:
            rect[3]

        padding = [left_padd, top_padd, right_padd, bottom_padd]
        roi = image[rect[2]:rect[3], rect[0]:rect[1]]

        return roi, start_roi, padding

    @staticmethod
    def get_small_roi(image, box):
        r_x = box.W
        r_y = box.H
        start_roi = (int(box.center[0] - int(r_x/2)), int(box.center[1] - int(r_y/2)))
        rect = [start_roi[0], int(box.center[0] + int(r_x/2)),
                start_roi[1], int(box.center[1] + int(r_y/2))]

        rect[0] = 0 if 0 > rect[0] else rect[0]
        rect[2] = 0 if 0 > rect[2] else rect[2]
        rect[1] = image.shape[1] if rect[1] > image.shape[1] else rect[1]
        rect[3] = image.shape[0] if rect[3] > image.shape[0] else rect[3]

        roi = image[rect[2]:rect[3], rect[0]:rect[1]]
        return roi

    # TODO try search on bitwise image
    def find_best_counters(self, roi, contours, padding):
        full_counters = []
        for cnt in contours:
            img_squere = roi.shape[0] * roi.shape[1]
            cnt_squere = cv2.contourArea(cnt)
            M = cv2.moments(cnt)
            center = None
            if M['m00'] != 0:
                center = (int(M['m10'] / M['m00']),
                          int(M['m01'] / M['m00']))
            x, y, w, h = cv2.boundingRect(cnt)
            if cnt_squere > img_squere * 0.70 or h < int((roi.shape[0]+padding[1]+padding[3]) * 0.5 / 6):
                continue
            cnt_image = cv2.drawContours(np.zeros(roi.shape[:2], dtype=np.uint8), [cnt], -1, 255, -1)
            temp = cnt_image[int((roi.shape[0]+padding[1]+padding[3]) / 4-padding[1]):int((roi.shape[0]+padding[1]+padding[3]) * 0.75 -padding[1]),
                   int((roi.shape[1]+padding[0]+padding[2]) / 4-padding[0]):int((roi.shape[1]+padding[0]+padding[2]) * 0.75-padding[0])]
            rect = (int((roi.shape[1]+padding[0]+padding[2]) / 4-padding[0]), int((roi.shape[0]+padding[1]+padding[3]) / 4-padding[1]),
                    int((roi.shape[1]+padding[0]+padding[2]) * 0.5), int((roi.shape[0]+padding[1]+padding[3]) * 0.5))
            if temp.max() == 255:
                if self.is_point_in_rect(center if center is not None else cv2.boundingRect(cnt)[:2], rect):
                    full_counters.append(cnt)
        return full_counters

    def create_holst_from_counters(self, roi, box, counters):
        holst = np.zeros(roi.shape[:2], dtype=np.uint8)
        holst = cv2.drawContours(holst, counters, -1, 255, -1)
        angle, holst = self.orientate(holst)
        holst = cv2.erode(holst, np.ones((3, 3), np.uint8), iterations=1)
        holst = cv2.dilate(holst, np.ones((3, 3), np.uint8), iterations=1)
        holst = box.cut_holst_from_bin_roi(holst)
        if self.debug_mode:
            show_image(holst, "cut holst")
        return angle, holst

    def get_rects_from_holst(self, counters, holst_shape, roi_shape):
        min_area = holst_shape[0] * holst_shape[1] * 0.1
        center = (roi_shape[0] // 2, roi_shape[1] // 2)
        rects = [cv2.boundingRect(ctr) for ctr in counters]
        rects = [r for r in rects if r[2] * r[3] > min_area]
        points = [(r[0] + int(r[2] / 2), r[1] + int(r[3] / 2))
                  for r in rects]
        zip_rects = rects.copy()
        for rect1 in rects:
            for point, rect2 in zip(points, zip_rects):
                if self.is_point_in_rect(point, rect1) and rect1 != rect2 and \
                                rect2 in rects and rect1[2] * rect1[3] > rect2[2] * rect2[3]:
                    rects.remove(rect2)
        return [r for r in rects if r[1] < center[1]]


    def check_bottom_line_in_contour(self, image, cnt):
        (h, w) = image.shape[:2]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        angle = rect[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        if angle < 0:
            _w = abs(box[0][0] - box[1, 0])
            _h = abs(box[1][1] - box[2, 1])
        else:
            _w = abs(box[3][0] - box[0, 0])
            _h = abs(box[0][1] - box[1, 1])

        if _h == 0:
            _h = 1
        bottom_line = False
        if _w / _h > 7 and _w > 0.7 * w and box[0][1] > 0.7 * h:
            bottom_line = True
        return bottom_line, angle

    def detect_and_delete_bottom_line(self, img):
        image = img.copy()
        (h, w) = image.shape[:2]
        show_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        image_n = cv2.bitwise_not(image)
        contours = cv2.findContours(image_n, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        for cnt in contours:
            bottom_line, angle = self.check_bottom_line_in_contour(image_n, cnt)
            if bottom_line:
                # стираем линию
                cv2.drawContours(image, [cnt], -1, (255, 255, 255), -1)
                # разворачиваем и возвращаем изображение
                new_img = cv2.bitwise_not(Binarizaion.rotate_img(image, angle), bottom_line)
                max = np.max(new_img, axis=1)
                crop = -1
                for i in range(len(max) - 1, 0, -1):
                    if max[i] > 0:
                        crop = i
                        break
                if crop != -1:
                    crop_img = new_img[0:crop + 2, 0:w - 1]
                return cv2.bitwise_not(crop_img), bottom_line

        max_x = np.full(w, -1)  # внимание на shape
        for x in range(w):
            for y in range(h):
                if image_n[y, x] > 0 and y > max_x[x]:
                    max_x[x] = y
        blank_image = np.zeros((h, w, 1), np.uint8)

        for x in range(len(max_x)):
            if max_x[x] >= 0:
                blank_image[max_x[x], x] = 255
        contours = cv2.findContours(blank_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        max_cnt = contours[0]
        for cnt in contours:
            if cv2.arcLength(cnt, True) > cv2.arcLength(max_cnt, True):
                max_cnt = cnt
        cv2.drawContours(show_img, [max_cnt], -1, (0, 255, 0), -1)
        bottom_line, angle = self.check_bottom_line_in_contour(image, max_cnt)
        if bottom_line:
            image_n = Binarizaion.rotate_img(image_n, angle)
        else:
            return image, bottom_line
        pix_sum = np.full(h, 0)
        for y in range(h):
            for x in range(w):
                if image_n[y][x] > 0:
                    pix_sum[y] = pix_sum[y] + 1
        local_min = -1
        for i in range(len(pix_sum) - 5, int(0.7 * h), -1):
            if pix_sum[i + 4] - pix_sum[i] < 0.2 * w:
                continue
            is_min = True
            for j in range(-4, 4):
                if j != 0:
                    if pix_sum[i] > pix_sum[i - j]:
                        is_min = False
                        break
            if is_min:
                local_min = i
                break
        if local_min != -1:
            image_n[local_min: h - 1, 0:w - 1] = 0
            crop_img = image_n[0:local_min + 2, 0:w - 1]
            return cv2.bitwise_not(crop_img), bottom_line
        return image, bottom_line

    def detect_merged_components(self, img):
        angle, image = self.orientate(img)
        h = image.shape[0]
        w = image.shape[1]
        image_n = cv2.bitwise_not(image)
        image_n = (image_n / 255).astype(int)
        sum = image_n.sum(axis=0)
        min = -1
        for i in range(int(0.3 * w), int(0.7 * w)):
            is_min = True
            left_big = False
            right_big = False
            for j in range(2, 10):
                # проверяем на локальный минимум в окрестности
                if sum[i - j] < sum[i]:
                    is_min = False
                    break
                if sum[i + j] < sum[i]:
                    is_min = False
                    break
                # проверяем что в окрестности есть производная больше 2 в окрестности
                if (sum[i + j] - sum[i + j - 2]) / 2 >= 2:
                    right_big = True
                if (sum[i - j] - sum[i - j + 2]) / 2 >= 2:
                    left_big = True
            if is_min and left_big and right_big and sum[i] < h / 6:
                min = i
                break
        if min != -1:
            cv2.line(image, (min, 0), (min, h), (255, 255, 255), 3)
        return image, min  # return -1 in min if all s good and local min if there is 2 merged components

