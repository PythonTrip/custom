import cv2
from .Image import Image
import numpy as np

image = Image()
rad = np.radians


class ImageObject:
    def __init__(self, area):
        super().__init__()
        self.area = area # Площадь объекта

    def get_objects(self, contours=None):
        if contours is None:
            contours = self.contour_filter(self.area)
        image.objects = []
        for contour in contours:
            contours_poly = self.approx_polly(contour)
            boundRect = cv2.boundingRect(contours_poly)
            center = self.moment_center(contour)
            if len(contours_poly) == 4:
                angle = self.get_angle(contours_poly)
                image.objects.append([center, angle, cv2.contourArea(contour), contours_poly, boundRect])

    @staticmethod
    def contour_filter(area):
        min, max = area
        contours, hierarchy = cv2.findContours(image.get_image(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filtered = []
        for contour in contours:
            if max > cv2.contourArea(contour) > min:
                filtered.append(contour)
        return filtered

    @staticmethod
    def approx_center(points):
        cX, cY = [(points[0][0][0] + points[1][0][0]) // 2, (points[0][0][1] + points[2][0][1]) // 2]
        return [cX, cY]

    @staticmethod
    def moment_center(contour):
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return [cX, cY]

    @staticmethod
    def approx_polly(contour):
        peri = cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, peri * 0.07, True)

    @staticmethod
    def get_angle(contours_poly):
        p1 = contours_poly[0][0]
        p2 = contours_poly[3][0]
        hc = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
        dy = abs(p1[1] - hc[1])
        dx = abs(p1[0] - hc[0])
        angle = (rad(90) - np.arctan(dx / dy)) if dy > 0 else 0
        return angle
