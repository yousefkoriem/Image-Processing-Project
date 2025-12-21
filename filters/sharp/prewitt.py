import cv2
import numpy as np


def Prewitt(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    grad_x = cv2.filter2D(gray, cv2.CV_64F, kernel_x)
    grad_y = cv2.filter2D(gray, cv2.CV_64F, kernel_y)

    grad_x = np.uint8(np.absolute(grad_x))
    grad_y = np.uint8(np.absolute(grad_y))

    prewitt_combined = cv2.bitwise_or(grad_x, grad_y)
    prewitt_combined_bgr = cv2.cvtColor(prewitt_combined, cv2.COLOR_GRAY2BGR)
    sharpened = cv2.add(img, prewitt_combined_bgr)

    return sharpened
