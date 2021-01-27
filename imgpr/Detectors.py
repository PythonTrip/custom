from abc import ABC, abstractmethod
import cv2
from .Image import Image
import imutils
import numpy as np
from pyzbar import pyzbar

image = Image()


# just nothing
def nothing(*arg):
    pass


def make_coordinates(image, line_parameters):
    # Y = MX + B
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []

    while lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        print('LEFT: ', left_fit_average)
        left_line = make_coordinates(image, left_fit_average)
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_coordinates(image, right_fit_average)
        print('RIGHT: ', right_fit_average)
        return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 7)
    return line_image


# Abstract on detection
class ADetection(ABC):
    def __init__(self, *args, **kwargs):
        ABC.__init__(self)

    @abstractmethod
    def update_img(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, *args, **kwargs): pass


class NoneDetection(ADetection):
    def __init__(self):
        super().__init__()

    def update_img(self):
        pass

    def post(self): pass


class TextAnalyze(ADetection):
    def __init__(self):
        super().__init__()

    def update_img(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class LineDetection(ADetection):
    def __init__(self):
        super().__init__()
        self.lines = []

    def update_img(self):
        image.set_image(cv2.GaussianBlur(image.get_image(), (5, 5), 0))
        image.set_image(cv2.Canny(image.get_image(), 50, 150))

    def post(self, rho, theta, threshold, minLineLength=None, maxLineGap=None):
        self.lines = cv2.HoughLinesP(image.get_image(), rho, theta, threshold,
                                     minLineLength, maxLineGap)
        self.lines = average_slope_intercept(image.get_image(), self.lines)


class QRDetection(ADetection):
    def __init__(self):
        super().__init__()

    def update_img(self):
        img = cv2.GaussianBlur(image.get_image(), (3, 3), 2)
        img = cv2.Canny(img, 240, 250)
        st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 35), (5, 5))
        st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, st1)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, st2)
        image.set_image(img)

    def post(self):
        out = image.get_image()
        for i, val in enumerate(image.objects):
            x, y, w, h = val[4]
            image.objects[i][4] = (x - 7, y - 7, w + 14, h + 14)
            roi = image.ROI(out.copy(), val[4])
            if not 0 in roi.shape:
                out = imutils.rotate(roi, np.degrees(val[1]))
                detectedBarcodes = pyzbar.decode(roi)
                cv2.imshow("123", out)
                if cv2.waitKey(0) == 27: pass
                if len(detectedBarcodes) > 0:
                    for barcode in detectedBarcodes:
                        print(barcode.data.decode())
            else:
                out = roi
        return out


class CircleDetection(ADetection):
    def __init__(self):
        super().__init__()

    def update_img(self):
        image.set_image(cv2.cvtColor(image.get_image(), cv2.COLOR_BGR2GRAY))
        image.set_image(cv2.Canny(image.get_image(), 180, 255))

    def post(self):
        circles = cv2.HoughCircles(image.get_image(), cv2.HOUGH_GRADIENT, 2, 1,
                                   np.array([]))
        if circles is not None and len(circles) > 0:
            maxRadius = 0
            x = 0
            y = 0

            for c in circles[0]:
                if c[2] > maxRadius:
                    maxRadius = int(c[2])
                    x = int(c[0])
                    y = int(c[1])
            return [x, y, maxRadius]
        else:
            return None


# Color detection implementation
class ColorDetection(ADetection):
    def __init__(self, hsv_min, hsv_max):
        super().__init__()
        self.hsv = [hsv_min, hsv_max]

    def post(self): pass

    def update_img(self):
        image.set_image(cv2.cvtColor(image.get_image(), cv2.COLOR_BGR2HSV))
        image.set_image(
            cv2.inRange(image.get_image(), self.hsv[0], self.hsv[1]))

    def createTrackbars(self):
        cv2.namedWindow("settings")  # create settings window
        cv2.createTrackbar('h1', 'settings', self.hsv[0][0], 255, nothing)
        cv2.createTrackbar('s1', 'settings', self.hsv[0][1], 255, nothing)
        cv2.createTrackbar('v1', 'settings', self.hsv[0][2], 255, nothing)
        cv2.createTrackbar('h2', 'settings', self.hsv[1][0], 255, nothing)
        cv2.createTrackbar('s2', 'settings', self.hsv[1][1], 255, nothing)
        cv2.createTrackbar('v2', 'settings', self.hsv[1][2], 255, nothing)

    def getHSV(self):
        self.hsv[0][0] = cv2.getTrackbarPos('h1', 'settings')
        self.hsv[0][1] = cv2.getTrackbarPos('s1', 'settings')
        self.hsv[0][2] = cv2.getTrackbarPos('v1', 'settings')
        self.hsv[1][0] = cv2.getTrackbarPos('h2', 'settings')
        self.hsv[1][1] = cv2.getTrackbarPos('s2', 'settings')
        self.hsv[1][2] = cv2.getTrackbarPos('v2', 'settings')
