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
from filters.noise import salt, pepper, salt_and_pepper


# ---------- Define filters ----------

def Salt():
    return lambda img: salt.Salt(img,0.15)
def Pepper():
    return lambda img: pepper.Pepper(img,0.15)
def Salt_and_Pepper():
    return lambda img: salt_and_pepper.Salt_and_Pepper(img,0.15)

FILTERS = [
    ("Salt Noise", Salt()),
    ("Pepper Noise", Pepper()),
    ("Salt and Pepper Noise", Salt_and_Pepper()),
]


def Noise(parent, image_bgr):
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
        title="Sharpening Filters",
        display_max_size=(800, 600),
        cumulative=True,
    )
