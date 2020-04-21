import cv2
import numpy as np


class Perspective:
    def __init__(self, src):
        self.dst = None
        self.pts_transformer = self.calc_transform_params(src)

    def transform_pts(self, pts):
        transformed_pts = cv2.perspectiveTransform(pts, self.pts_transformer)
        return transformed_pts

    def calc_transform_params(self, src):
        (tl, tr, br, bl) = src

        # Compute width of new image
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        self.maxWidth = max(int(widthA), int(widthB))

        # Compute height of new image
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        self.maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [self.maxWidth - 1, 0],
            [self.maxWidth - 1, self.maxHeight - 1],
            [0, self.maxHeight - 1]], dtype="float32")

        self.dst = dst

        pts_transformer, _ = cv2.findHomography(src, dst)

        return pts_transformer
