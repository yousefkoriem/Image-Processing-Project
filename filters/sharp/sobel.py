import cv2
import numpy as np
from tkinter import simpledialog

def Sobel(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    kernel = simpledialog.askinteger(title="Kernel Size", prompt="Enter a Kernel length",minvalue=1,maxvalue=21)
    kernel += kernel&1^1
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, kernel)

    sobelx = np.uint8(np.absolute(sobelx))
    sobely = np.uint8(np.absolute(sobely))

    sobel_combined = cv2.bitwise_or(sobelx, sobely)
    sobel_combined_bgr = cv2.cvtColor(sobel_combined, cv2.COLOR_GRAY2BGR)
    sharpened = cv2.add(img, sobel_combined_bgr)

    return sharpened
