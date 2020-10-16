import cv2
import numpy as np


class Image:
    def __init__(self):
        self.img = None
        self.objects = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Image, cls).__new__(cls)
        return cls.instance

    def scale_resize(self, scale, interpolation=cv2.INTER_AREA):
        width = int(self.img.shape[1] * scale)
        height = int(self.img.shape[0] * scale)
        self.img = cv2.resize(self.img, (width, height), interpolation=interpolation)

    def set_image(self, img):
        self.img = img

    def get_image(self):
        return self.img

    def region(self, vertices):
        mask = np.zeros_like(self.img)
        cv2.fillPoly(mask, vertices, 1024)
        self.img = cv2.bitwise_and(self.img, mask)

    def mask(self):
        height = self.img.shape[0]
        pts = np.array([[650, height // 1.7], [1000, height // 1.7], [1200, 700], [600, 700]], np.int64)
        mask = np.zeros_like(self.img)
        channel_count = self.img.shape[2]
        match_mask = (255,) * channel_count
        cv2.fillPoly(mask, np.array([pts], dtype=np.int64), match_mask)
        self.img = cv2.bitwise_and(self.img, mask)

    def ROI(self, img, rectangle):
        self.img = img[int(rectangle[1]):int(rectangle[1] + rectangle[3]),
                   int(rectangle[0]):int(rectangle[0] + rectangle[2])]

    def black_white_filling(self):
        white = sum((self.get_image() / 255).ravel())
        WH = self.img.width * self.img.height
        return white / WH * 100

    @property
    def width(self):
        return self.img.shape[1]

    @property
    def height(self):
        return self.img.shape[0]

    @staticmethod
    def coordinates_ROI2FRAME(roi, xy):
        x, y = xy
        return [x + roi[0], y + roi[1]]

