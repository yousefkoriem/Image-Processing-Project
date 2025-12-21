import numpy as np
import cv2 

def Min(img, kernel):
    kernel = np.ones((kernel, kernel), np.uint8)
    pepper = cv2.erode(img, kernel)
    return pepper
