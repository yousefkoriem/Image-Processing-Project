"""
example_app.py

Minimal example that imports filter_toolkit and uses show_filter_session.
Run this with a Tk-capable environment (on WSL make sure python3-tk is installed).
"""

import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from .assets.filter_toolkit import show_filter_session


# ---------- Define filters ----------

def laplacian():
    return lambda img: cv2.Laplacian(img, cv2.CV_64F)
def sobel():
    return lambda img: cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
def prewitt():
    kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
    kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    return lambda img: cv2.filter2D(cv2.filter2D(img, -1, kernelx), -1, kernely)

FILTERS = [
    ("Laplacian", laplacian()),
    ("Sobel",sobel()),
    ("Prewitt", prewitt()),
]


def Sharp(parent, image_bgr):
    """
    Entry point for the smoothing genre.
    The main UI should call ONLY this function.

    Parameters:
        parent     : tk root or tk window
        image_bgr  : OpenCV image (BGR)

    Returns:
        np.ndarray (BGR) if user applied filters
        None if user cancelled
    """
    image_bgr = cv2.resize(image_bgr, (300, 400))
    return show_filter_session(
        parent,
        image_bgr,
        FILTERS,
        title="Sharpening Filters",
        display_max_size=(800, 600),
        cumulative=True,
    )
