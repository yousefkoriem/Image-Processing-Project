import cv2
import numpy as np

def Laplacian(image):
    b, g, r = cv2.split(image)
    lap_b = cv2.Laplacian(b, cv2.CV_64F)
    lap_g = cv2.Laplacian(g, cv2.CV_64F)
    lap_r = cv2.Laplacian(r, cv2.CV_64F)

    sharp_b = np.clip(b + lap_b, 0, 255).astype(np.uint8)
    sharp_g = np.clip(g + lap_g, 0, 255).astype(np.uint8)
    sharp_r = np.clip(r + lap_r, 0, 255).astype(np.uint8)

    sharpened = cv2.merge([sharp_b, sharp_g, sharp_r])
    return sharpened
