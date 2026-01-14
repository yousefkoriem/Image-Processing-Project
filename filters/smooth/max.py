import numpy as np
import cv2
from tkinter import simpledialog


def Max(img):
    ksize = simpledialog.askinteger(
        title="Kernel Size", prompt="Enter a Kernel length",initialvalue=3, minvalue=1, maxvalue=21
    )
    ksize += ksize & 1 ^ 1
    kernel = np.ones((ksize, ksize), np.uint8)
    pepper = cv2.dilate(img, kernel)
    return pepper
