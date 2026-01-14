import numpy as np
import cv2
from tkinter import simpledialog


def Mean(img):
    ksize = simpledialog.askinteger(title="Kernel Size", prompt="Enter a Kernel length",initialvalue=3, minvalue=1,maxvalue=21)
    ksize += ksize&1^1
    kernel = ksize
    mean_filtered = cv2.blur(img, (kernel, kernel))
    return mean_filtered
