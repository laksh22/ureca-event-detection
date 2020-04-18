import cv2
import numpy as np


class Perspective:
    def __init__(self, image, src):
        self.image_transformer, self.pts_transformer = self.calc_transform_params(
            image, src)

    def transform_img(self, image):
        transformed_img = cv2.warpPerspective(
            image, self.image_transformer, (self.maxWidth, self.maxHeight))
        return transformed_img

    def transform_pts(self, pts):
        transformed_pts = cv2.perspectiveTransform(pts, self.pts_transformer)

    def calc_transform_params(self, image, pts):
        rect = self.order_pts(pts)
        (tl, tr, br, bl) = rect

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

        img_transformer = cv2.getPerspectiveTransform(rect, dst)
        pts_transformer, _ = cv2.findHomography(rect, dst)

        return img_transformer, pts_transformer

    def order_pts(self, pts):
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect
