import cv2
import numpy as np

def Pepper(image ,pepper_prob = 0.01 ):
    noisy_image = image.copy()
    pepper_mask = np.random.random(image.shape) < pepper_prob
    noisy_image[pepper_mask] = 0
    return noisy_image