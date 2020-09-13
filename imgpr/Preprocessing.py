import cv2
import numpy as np
from .Detectors import ADetection
from .Image import image


# Обработка изображения
class ImageProcessing:
    def __init__(self, detection: ADetection):
        self.detect = detection

    # Invoke actions
    def transform(self, actions=None):
        self.detect.update_img()
        if actions is not None:
            for action, params in actions:
                action.main(params)


# События мыши
class MouseCallback:
    def __init__(self):
        self.xy = []
        self.vectors = []

    def set_points(self, event, x, y, flags, param):
        if event == cv2.EVENT_RBUTTONDOWN:
            if len(self.xy) > 0:
                lx, ly = self.xy[len(self.xy) - 1]
                self.vectors.append([lx, ly, x, y])
                self.xy.pop(len(self.xy) - 1)
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print(x, y)
            self.xy.append([x, y])


# Отрисовка на изображении
class Draw:
    @staticmethod
    def draw_points(frame, xy):
        [cv2.circle(frame, (int(x), int(y)), 3, (255, 255, 250)) for x, y in xy]

    @staticmethod
    def draw_rectangle(frame, rectangle):
        cv2.rectangle(frame, (rectangle[0], rectangle[1]),
                      (rectangle[0] + rectangle[2], rectangle[1] +
                       rectangle[3]), (0, 0, 0), 2)

    @staticmethod
    def draw_vectors(frame, vectors):
        [cv2.line(frame, (int(vector[0]), int(vector[1])), (int(vector[2]), int(vector[3])), (255, 255, 255), 2)
         for vector in vectors]

    @staticmethod
    def draw_centers(frame):
        for center, angle, area, contours_poly, rect in image.objects:
            cv2.circle(frame, (int(center[0]), int(center[1])), 3, (255, 255, 0))

    @staticmethod
    def draw_rectangles(frame):
        for _, _, _, _, boundRect in image.objects:
            cv2.rectangle(frame, (int(boundRect[0]), int(boundRect[1])),
                          (int(boundRect[0] + boundRect[2]), int(boundRect[1] +
                                                                 boundRect[3])), (0, 0, 0), 2)

    @staticmethod
    def draw_angles(frame):
        for obj in image.objects:
            center, angle, _, contours_poly, _ = obj
            if len(contours_poly) == 4:
                p2 = int(center[0] + 50 * np.cos(angle)), int(center[1] + 50 * np.sin(angle))
                cv2.line(frame, (int(center[0]), int(center[1])), p2,
                         (255, 0, 0), 3)
                cv2.line(frame, (int(center[0]), int(center[1])),
                         (int(center[0] + 50 * np.cos(0)), int(center[1] + 50 * np.sin(0))),
                         (255, 0, 0), 3)
