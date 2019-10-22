from imutils import perspective
from matplotlib import pyplot as plt

import numpy as np
import cv2

from common.utils import resize_to_show


def remove_white():
    pass
    # return image


class RectangleSegmentation(object):
    def __init__(self):
        #  HSV masks for red/ yellow colors
        # Yellow mask
        self.lower_yel = np.array([18, 100, 100])
        self.upper_yel = np.array([60, 255, 255])
        self.yellow_mask = None
        # Lower red mask (0-10)
        self.lower_red1 = np.array([0, 50, 50])
        self.upper_red1 = np.array([10, 255, 255])
        # Upper red mask (170-180)
        self.lower_red2 = np.array([170, 50, 50])
        self.upper_red2 = np.array([180, 255, 255])
        self.red_mask = None

        # https://stackoverflow.com/questions/48182791/how-do-you-lightness-thresh-hold-with-hsl-on-opencv
        self.white_mask = None
        self.resized_image = None
        self.gray = None
        self.hsv = None

        self.size_img = 600
        # UP CONTRAST
        # img_yuv = cv2.cvtColor(temp, cv2.COLOR_BGR2YUV)
        # # equalize the histogram of the Y channel
        # img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        # # convert the YUV image back to RGB format
        # temp = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)


    def detect_price_type(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask0 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask1 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask_yellow = cv2.inRange(hsv, self.lower_yel, self.upper_yel)
        mask_red = mask0+mask1
        
        red_score = np.sum(mask_red > 0)
        yellow_score = np.sum(mask_yellow > 0)
        if yellow_score > red_score:
            return "card"
        else:
            return "sail"

    def is_red_or_yell(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask0 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask1 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask_yellow = cv2.inRange(hsv, self.lower_yel, self.upper_yel)
        mask_red = mask0 + mask1

        red_score = np.sum(mask_red > 0)
        yellow_score = np.sum(mask_yellow > 0)
        max_score = image.shape[0] * image.shape[1]
        if yellow_score > max_score * 0.3 or red_score > max_score * 0.3:
            return True
        else:
            return False

    def get_color(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask0 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask1 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask_yellow = cv2.inRange(hsv, self.lower_yel, self.upper_yel)
        mask_red = mask0 + mask1
        red_score = np.sum(mask_red > 0)
        yellow_score = np.sum(mask_yellow > 0)
        if yellow_score > red_score:
            return cv2.mean(image, mask=mask_yellow)
        else:
            return cv2.mean(image, mask=mask_red)


    def find_red(self, image):
        # pre proc up to prev lvl funk on stack
        # Apply yellow mask


        # Apply lower mask (0-10) and upper mask (170-180)
        mask0 = cv2.inRange(hsv, self.lower_red1, self.upper_red2)
        mask1 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask_red = mask0 + mask1

        mask, pts = self.find_rect(image, mask_red, "red")
        return mask, pts

    def find_white(self, img):
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        # equalize the histogram of the Y channel
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        # convert the YUV image back to RGB format
        img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        Lchannel = hls[:, :, 1]
        mask = cv2.inRange(Lchannel, 200, 255)

    def find_yellow(self, image):
        # Apply yellow mask
        mask_yellow = cv2.inRange(self.hsv, self.lower_yel, self.upper_yel)

        mask, pts = self.find_rect(image, mask_yellow, "yel")
        return mask, pts

    def find_rect(self, rgb_img, mask, color):
        kernel = np.ones((3, 3), np.uint8)

        mask = cv2.dilate(mask, kernel, iterations=3)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.04*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if area > 1000:
                if len(approx) == 4:
                    cv2.drawContours(rgb_img, [approx], 0, (0, 0, 0), 3)

                    cv2.putText(rgb_img, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX,
                                1, (0, 0, 0))
                    pts = np.array(approx.reshape(4, 2))
                    for (x, y) in pts:
                        cv2.circle(rgb_img, (x, y), 6, (0, 255, 0), -1)
                    warped = perspective.four_point_transform(rgb_img, pts)
                    cv2.imshow("warped", resize_to_show(warped))
                else:
                    pts = np.array(approx.reshape(len(approx), 2))
                    cv2.drawContours(rgb_img, [approx], 0, (0, 0, 0), 3)
                    for (x, y) in pts:
                        cv2.circle(rgb_img, (x, y), 6, (0, 255, 0), -1)

            cv2.imshow("Frame " + color, resize_to_show(rgb_img))
            cv2.imshow("Mask " + color, resize_to_show(mask))
            cv2.waitKey()
        return mask, None  # pts

    @staticmethod
    def is_correct_rectangle(rect):
        x, y, x1, y1, x2, y2, x3, y3 = rect
        if rect:
            return True
        return False

    def get_backgruound(self, img, rect=(50, 50, 450, 290)):
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        return img

    def do_best_for_shop(self, price_image):
        # self.resized_gray = cv2.resize(self.gray, (self.size_img, int(self.size_img * c)))

        c = price_image.shape[0] / price_image.shape[1]
        self.resized_image = cv2.resize(price_image, (self.size_img, int(self.size_img * c)))
        cv2.imshow("img", self.resized_image)


# # load the notecard code image, clone it, and initialize the 4 points
# # that correspond to the 4 corners of the notecard
# pts = np.array([(2000, 305), (1850, 265 + 1100), (730, 265), (730, 265 + 1140)])
#
# # loop over the points and draw them on the cloned image
# for (x, y) in pts:
#     cv2.circle(clone, (x, y), 9, (0, 255, 0), -1)
#
# # apply the four point tranform to obtain a "birds eye view" of
# # the notecard
# warped = perspective.four_point_transform(notecard, pts)
#
# # show the original and warped images
# cv2.imshow("Original", show_size(clone))
# cv2.imshow("Warped", show_size(warped))
# cv2.waitKey(1)
#
# coef = clone.shape[0] / clone.shape[1]
# size_img = int(clone.shape[0] / 5)
# clone = cv2.resize(clone, (size_img, int(size_img * coef)))
#
# gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# edgeMap = auto_canny(gray, sigma=0.1)
# cv2.imshow("Edge Map", show_size(edgeMap))
#
# gray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)
# edgeMap = auto_canny(gray, sigma=0.01)
# cv2.imshow("Edge Map 2", show_size(edgeMap))
#
# edgeMap = auto_canny(gray, sigma=0.01)
# (thresh, img_bin) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imshow("img_bin Map 2", show_size(img_bin))
#
# k = int(gray.shape[0]/20) if int(gray.shape[0]/30) % 2 != 0 else int(gray.shape[0]/20) + 1
# blur = cv2.GaussianBlur(clone, (7, 7), 1.07)
# cv2.imshow("Blur", show_size(blur))
#
# edges = cv2.Canny(blur, 160, 200)
# cv2.imshow("Blur Edge", show_size(edges))
#
#
# def gftt(edges):
#     corners = cv2.goodFeaturesToTrack(edges, 100, 0.01, 10, 100)
#     for i in corners:
#         x, y = i.ravel()
#         cv2.circle(gray, (int(x), int(y)), 3, (0, 255, 0), 2)
#     cv2.imshow("Edges gftt", show_size(gray))
#
#
#
# gftt(np.copy(edges))
# cv2.waitKey(0)

def main(image, shop):
    def nothing(x):
        print(x)

    def create_trackbar():
        cv2.namedWindow(COLOR_MASK)
        cv2.createTrackbar("L-H", COLOR_MASK, 0, 360, nothing)
        cv2.createTrackbar("L-S", COLOR_MASK, 0, 250, nothing)
        cv2.createTrackbar("L-V", COLOR_MASK, 0, 250, nothing)
        cv2.createTrackbar("U-H", COLOR_MASK, 0, 360, nothing)
        cv2.createTrackbar("U-S", COLOR_MASK, 0, 250, nothing)
        cv2.createTrackbar("U-V", COLOR_MASK, 0, 250, nothing)

        cv2.namedWindow(IMG_SETTINGS)
        cv2.createTrackbar("Blur", IMG_SETTINGS, 0, 1000, nothing)
        cv2.createTrackbar("Size", IMG_SETTINGS, 100, 2000, nothing)
        cv2.createTrackbar("canny_low", IMG_SETTINGS, 0, 255, nothing)
        cv2.createTrackbar("canny_upp", IMG_SETTINGS, 0, 255, nothing)
        cv2.createTrackbar("thr", IMG_SETTINGS, 0, 255, nothing)

    def update_trackbars():
        return int(cv2.getTrackbarPos("thr", IMG_SETTINGS)), \
               float(cv2.getTrackbarPos("Blur", IMG_SETTINGS)) / 100, \
               400 if cv2.getTrackbarPos("Size", IMG_SETTINGS) < 300 else cv2.getTrackbarPos("Size", IMG_SETTINGS), \
               int(cv2.getTrackbarPos("canny_low", IMG_SETTINGS)), \
               int(cv2.getTrackbarPos("canny_upp", IMG_SETTINGS)), \
               cv2.getTrackbarPos("L-H", COLOR_MASK), \
               cv2.getTrackbarPos("L-S", COLOR_MASK), \
               cv2.getTrackbarPos("L-V", COLOR_MASK), \
               cv2.getTrackbarPos("U-H", COLOR_MASK), \
               cv2.getTrackbarPos("U-S", COLOR_MASK), \
               cv2.getTrackbarPos("U-V", COLOR_MASK)

    create_trackbar()

    histr = cv2.calcHist([image], [0], None, [256], [0, 256])
    plt.plot(histr, color='r')
    plt.xlim([0, 256])
    plt.show()
    while True:
        thr_l, blur_k, size_img, cany_l, cany_u, l_h, l_s, l_v, u_h, u_s, u_v = update_trackbars()
        if shop == SUPERMARKET[0]:

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            coef = image.shape[0] / image.shape[1]
            temp = cv2.resize(gray, (size_img, int(size_img * coef)))

            cv2.imshow("gray", temp)
            cv2.imshow("edges", cv2.Canny(temp, cany_l, cany_u))

            frame = np.copy(temp)
            frame = cv2.GaussianBlur(frame, (7, 7), blur_k)

            ret, thresh = cv2.threshold(frame, thr_l, 255, cv2.THRESH_TOZERO)

            cv2.imshow("thresh", thresh)
            cv2.imshow("frame", frame)

            histr = cv2.calcHist([frame], [0], None, [256], [0, 256])
            plt.plot(histr, color='r')
            plt.xlim([0, 256])
            plt.draw()

        if shop == SUPERMARKET[1]:

            # UP CONTRAST
            # img_yuv = cv2.cvtColor(temp, cv2.COLOR_BGR2YUV)
            # # equalize the histogram of the Y channel
            # img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            # # convert the YUV image back to RGB format
            # temp = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

            coef = image.shape[0] / image.shape[1]
            temp = cv2.resize(image, (size_img, int(size_img * coef)))
            cv2.imshow("edges", cv2.Canny(temp, cany_l, cany_u))

            frame = np.copy(temp)
            frame = cv2.GaussianBlur(frame, (7, 7), blur_k)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # trackbars color HSV
            # upper = np.array([u_h, u_s, u_v])
            # lower = np.array([l_h, l_s, l_v])
            mask_custom = cv2.inRange(hsv, np.array([l_h, l_s, l_v]), np.array([u_h, u_s, u_v]))
            # lower_yel = np.array([18, 100, 100])
            # upper_yel = np.array([60, 255, 255])
            mask_yellow = cv2.inRange(hsv, np.array([18, 100, 100]), np.array([60, 255, 255]))
            # lower mask (0-10)
            mask0 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
            # upper mask (170-180)
            mask1 = cv2.inRange(hsv, np.array([170, 50, 50]), np.array([180, 255, 255]))
            # join my masks
            mask_red = mask0 + mask1

            for mask, color in ([mask_custom, "custom"],
                                [mask_yellow, "yellow"],
                                [mask_red, "red"]):
                find_rect(np.copy(frame), mask, color)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyAllWindows()

    result = ""
    return result


COLOR_MASK = "color_settings"
IMG_SETTINGS = "image_settings"
SUPERMARKET = {0: "FIVE", 1: "LENTA"}

if __name__ == '__main__':
    res = main(cv2.imread("Datasets\\datasets\\Lenta1\\1.jpeg"), SUPERMARKET[0])
    print(res)
