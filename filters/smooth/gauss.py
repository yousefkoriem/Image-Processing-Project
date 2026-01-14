import cv2
from tkinter import simpledialog


def Gaussian(img):
    ksize = simpledialog.askinteger(
        title="Kernel Size", prompt="Enter a Kernel length",initialvalue=3, minvalue=1, maxvalue=21
    )
    ksize += ksize & 1 ^ 1
    gauss = cv2.GaussianBlur(img, (ksize, ksize), 0)
    return gauss
