"""
example_app.py

Minimal example that imports filter_toolkit and uses show_filter_session.
Run this with a Tk-capable environment (on WSL make sure python3-tk is installed).
"""

import cv2
from .assets.filter_toolkit import show_filter_session
from filters.sharp import laplace, sobel, prewitt


# ---------- Define filters ----------


def Laplacian():
    return lambda img: laplace.Laplacian(img)


def Sobel():
    return lambda img: sobel.Sobel(img)


def Prewitt():
    return lambda img: prewitt.Prewitt(img)


FILTERS = [
    ("Laplacian", Laplacian()),
    ("Sobel", Sobel()),
    ("Prewitt", Prewitt()),
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
    image_bgr = cv2.resize(image_bgr, (500, 500))
    return show_filter_session(
        parent,
        image_bgr,
        FILTERS,
        title="Sharpening Filters",
        display_max_size=(800, 600),
        cumulative=True,
    )
