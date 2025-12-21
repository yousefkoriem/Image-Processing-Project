
import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from skimage.util import random_noise
from filter_toolkit import show_filter_session

def Add_pepper_noise ( image , pepper_prob = 0.01 ):
    noisy_image = image.copy()
    pepper_mask = np.random.random ( image.shape ) < pepper_prob
    noisy_image [ pepper_mask ] = 0
    return noisy_image