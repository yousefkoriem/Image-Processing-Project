import cv2
import numpy as np

def Salt_and_Pepper( image , salt_prob = 0.01 , pepper_prob = 0.01 ):
    noisy_image = image.copy()
    salt_mask = np.random.random ( image.shape ) < salt_prob
    noisy_image[ salt_mask ] = 255
    pepper_mask = np.random.random ( image.shape ) < pepper_prob
    noisy_image[ pepper_mask ] = 0
    return noisy_image
