"""
example_app.py

Minimal example that imports filter_toolkit and uses show_filter_session.
Run this with a Tk-capable environment (on WSL make sure python3-tk is installed).
"""

import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from assets.filter_toolkit import show_filter_session


# ---------- Define filters ----------
def gaussian_full(k=7):
    return lambda img: cv2.GaussianBlur(img, (k, k), 0)


def gaussian_preview():
    return lambda img: cv2.GaussianBlur(img, (5, 5), 0)


def sharpen():
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    return lambda img: cv2.filter2D(img, -1, kernel)


def add_noise(amount=0.03):
    def f(img):
        out = img.astype(np.float32) / 255.0
        out = np.clip(out + np.random.randn(*out.shape) * amount, 0.0, 1.0)
        return (out * 255).astype(np.uint8)

    return f


FILTERS = [
    ("Gaussian Blur (HQ)", gaussian_full(9), gaussian_preview()),
    ("Sharpen", sharpen()),
    ("Tiny Noise", add_noise(0.02)),
    ("Invert", lambda img: cv2.bitwise_not(img)),
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
    return show_filter_session(
        parent,
        image_bgr,
        FILTERS,
        title="Smoothing Filters",
        display_max_size=(800, 600),
        cumulative=True,
    )
