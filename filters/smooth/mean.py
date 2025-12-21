import numpy as np
import cv2


def Mean(img, kernel):
    mean_filtered = cv2.blur(img, (kernel, kernel))
    return mean_filtered
