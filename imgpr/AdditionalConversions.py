import cv2
from abc import ABC, abstractmethod
from .Image import Image

image = Image()


class ATransform(ABC):
    def __init__(self): pass

    @abstractmethod
    def main(self, params): pass


class Backsub(ATransform):
    def __init__(self, backsub=cv2.createBackgroundSubtractorMOG2, bs_params=None):
        super().__init__()
        if bs_params is None:
            bs_params = list()
        self.backsub = backsub(*bs_params)

    # subtract background
    def main(self, params):
        image.set_image(self.backsub.apply(image.get_image()))


class Morphology(ATransform):
    def __init__(self):
        super().__init__()

    # morph transform
    def main(self, params):
        if not params is None:
            st1 = cv2.getStructuringElement(cv2.MORPH_RECT, **params[0])
            st2 = cv2.getStructuringElement(cv2.MORPH_RECT, **params[1])
        else:
            st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15), (3, 3))
            st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

        image.set_image(cv2.morphologyEx(image.get_image(), cv2.MORPH_CLOSE, st1))
        image.set_image(cv2.morphologyEx(image.get_image(), cv2.MORPH_OPEN, st2))
