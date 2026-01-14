"""
example_app.py

Minimal example that imports filter_toolkit and uses show_filter_session.
Run this with a Tk-capable environment (on WSL make sure python3-tk is installed).
"""

import cv2
from .assets.filter_toolkit import show_filter_session
from filters.smooth import min, max, gauss, mean, median
from tkinter import simpledialog


# ---------- Define filters ----------
def Min():
    
    return lambda img: min.Min(img)
def Max():
    return lambda img: max.Max(img)
def Gaussian():
    return lambda img: gauss.Gaussian(img)
def Mean():
    return lambda img: mean.Mean(img)
def Median():
    return lambda img: median.Median(img)

FILTERS = [
    ("Gaussian Blur (HQ)", Gaussian()),
    ("Mean Filter", Mean()),
    ("Median Filter", Median()),
    ("Min Filter", Min()),
    ("Max Filter", Max()),
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
