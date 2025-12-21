import numpy as np
import cv2

def Median(img, kernel):
    img = cv2.medianBlur(img, kernel)
    return img