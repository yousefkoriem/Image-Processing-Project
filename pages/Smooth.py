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
from filters.smooth import min, max, gauss, mean, median


# ---------- Define filters ----------
def Min(ksize=3):
    return lambda img: min.Min(img, ksize)
def Max(ksize=3):
    return lambda img: max.Max(img, ksize)
def Gaussian(ksize=3):
    return lambda img: gauss.Gaussian(img, ksize)
def Mean(ksize=3):
    return lambda img: mean.Mean(img, ksize)
def Median(ksize=3):
    return lambda img: median.Median(img, ksize)

FILTERS = [
    ("Gaussian Blur (HQ)", Gaussian(3)),
    ("Mean Filter", Mean(3)),
    ("Median Filter", Median(3)),
    ("Min Filter", Min(3)),
    ("Max Filter", Max(3)),
]


def Smooth(parent, image_bgr):
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
    image_bgr = cv2.resize(image_bgr, (500, 500))
    return show_filter_session(
        parent,
        image_bgr,
        FILTERS,
        title="Smoothing Filters",
        display_max_size=(800, 600),
        cumulative=True,
    )
