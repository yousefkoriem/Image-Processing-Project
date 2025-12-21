import numpy as np
import cv2

def Max(img, kernal):
    kernel = np.ones((kernal, kernal), np.uint8)
    pepper = cv2.dilate(img, kernel)
    return pepper