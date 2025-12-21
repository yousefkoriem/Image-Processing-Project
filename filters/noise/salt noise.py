import cv2
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Image
from skimage.util import random_noise



def Add_salt_noise ( image , salt_prob = 0.01 ):
    noisy_image = image.copy()
    salt_mask = np.random.random ( image.shape ) < salt_prob
    noisy_image [ salt_mask ] = 255
    return noisy_image