import cv2
import numpy as np

def Salt(image ,salt_prob = 0.01):
    noisy_image = image.copy()
    salt_mask = np.random.random(image.shape) < salt_prob
    noisy_image[salt_mask] = 255
    return noisy_image