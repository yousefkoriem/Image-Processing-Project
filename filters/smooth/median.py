import numpy as np
import cv2
from tkinter import simpledialog

def Median(img):
    ksize = simpledialog.askinteger(title="Kernel Size", prompt="Enter a Kernel length",initialvalue=3, minvalue=1,maxvalue=21)
    ksize += ksize&1^1
    kernel = ksize
    img = cv2.medianBlur(img, kernel)
    return img