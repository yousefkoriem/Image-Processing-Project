"""
filter_toolkit.py

Reusable module that shows a modal filter popup (Tkinter) for OpenCV images.

Exports:
    - FilterSession(parent, filters, image_bgr, **kwargs)
    - show_filter_session(parent, image_bgr, filters, **kwargs)

Filters descriptors accepted:
    - ("Name", func)                 # func used for both preview and full
    - ("Name", full_func, preview_func)
    - {"name": "Name", "full": full_func, "preview": preview_func}

All filter functions must accept and return a BGR numpy array (OpenCV convention).
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Sequence, Tuple, Callable, Optional, Union, Dict, Any, List
import numpy as np
from PIL import Image, ImageTk
import cv2
import warnings

ArrayLike = np.ndarray
FilterFunc = Callable[[ArrayLike], ArrayLike]
FilterDescriptor = Union[Tuple[str, FilterFunc], Tuple[str, FilterFunc, FilterFunc], Dict[str, Any]]


# -------------------- Utilities --------------------
def _ensure_bgr_uint8(img: ArrayLike) -> ArrayLike:
    """Normalize image to HxWx3 uint8 BGR."""
    if img is None:
        raise ValueError("image is None")
    arr = np.asarray(img)
    if np.issubdtype(arr.dtype, np.floating):
        # assume in 0..1 range
        arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    else:
        arr = arr.astype(np.uint8)
    if arr.ndim == 2:
        arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    elif arr.ndim == 3 and arr.shape[2] == 1:
        arr = cv2.cvtColor(arr[:, :, 0], cv2.COLOR_GRAY2BGR)
    elif arr.ndim == 3 and arr.shape[2] == 3:
        pass
    else:
        raise ValueError(f"Unsupported image shape: {arr.shape}")
    return arr


def _fit_image_bgr(img_bgr: ArrayLike, max_size=(640, 480)) -> ArrayLike:
    """Resize image to fit inside max_size keeping aspect ratio."""
    h, w = img_bgr.shape[:2]
    max_w, max_h = max_size
    scale = min(max_w / w, max_h / h, 1.0)
    if scale < 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        return cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img_bgr.copy()


def _bgr_to_photoimage(img_bgr: ArrayLike) -> ImageTk.PhotoImage:
    """Convert BGR numpy image to Tk PhotoImage (via PIL)."""
    img = _ensure_bgr_uint8(img_bgr)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    return ImageTk.PhotoImage(pil)


def _normalize_descriptor(desc: FilterDescriptor) -> Tuple[str, FilterFunc, FilterFunc]:
    """
    Normalize a filter descriptor to (name, full_func, preview_func).
    Accepts:
      - (name, func)
      - (name, full_func, preview_func)
      - {"name":..., "full":..., "preview":...}
    """
    if isinstance(desc, dict):
        name = desc.get("name")
        full = desc.get("full")
        preview = desc.get("preview", full)
        if name is None or full is None:
            raise ValueError("dict descriptor requires 'name' and 'full'")
        return name, full, preview
    if isinstance(desc, (tuple, list)):
        if len(desc) == 2:
            name, f = desc
            return name, f, f
        if len(desc) == 3:
            name, full, preview = desc
            return name, full, preview
    raise ValueError("Filter descriptor must be (name, func) or (name, full, preview) or dict")


# -------------------- Main combined class --------------------
class FilterSession:
    """
    Combined popup + genre behavior.

    Constructor:
        FilterSession(parent,
                      filters: Sequence[FilterDescriptor],
                      image_bgr: np.ndarray,
                      *,
                      display_max_size=(640,480),
                      cumulative=True,
                      title="Filters",
                      button_width=18,
                      resizable=False)

    Methods:
        run() -> Optional[np.ndarray]
            Shows modal popup, returns full-resolution processed BGR array (or None if canceled).
    """
    def __init__(
        self,
        parent,
        filters: Sequence[FilterDescriptor],
        image_bgr: ArrayLike,
        *,
        display_max_size=(640, 480),
        cumulative: bool = True,
        title: str = "Filters",
        button_width: int = 18,
        resizable: bool = False,
    ):
        self.parent = parent
        self.title = title
        self.display_max_size = display_max_size
        self.cumulative = cumulative
        self.button_width = button_width
        self.resizable = resizable

        # Normalize filters
        self._filters: List[Tuple[str, FilterFunc, FilterFunc]] = []
        for d in filters:
            name, full, preview = _normalize_descriptor(d)
            if not callable(full) or not callable(preview):
                raise ValueError(f"Filter functions for '{name}' must be callable")
            self._filters.append((name, full, preview))

        # images
        self.base_full = _ensure_bgr_uint8(image_bgr)
        self.base_display = _fit_image_bgr(self.base_full, max_size=self.display_max_size)
        self.preview_display = self.base_display.copy()

        # chains for replay
        self._full_chain: List[FilterFunc] = []
        self._preview_chain: List[FilterFunc] = []

        # result image after Apply
        self._result: Optional[ArrayLike] = None

        # tkinter image refs to avoid GC
        self._tk_base = None
        self._tk_preview = None

        # toplevel created on run()
        self.top: Optional[tk.Toplevel] = None

    # ---- internal UI helpers ----
    def _update_base_widget(self, label_widget: ttk.Label):
        self._tk_base = _bgr_to_photoimage(self.base_display)
        label_widget.configure(image=self._tk_base)

    def _update_preview_widget(self, label_widget: ttk.Label):
        self._tk_preview = _bgr_to_photoimage(self.preview_display)
        label_widget.configure(image=self._tk_preview)

    def _on_filter_click(self, full_func: FilterFunc, preview_func: FilterFunc, name: str, preview_label: ttk.Label):
        """Handle filter button click: update preview and store chain."""
        try:
            if self.cumulative:
                new_preview = preview_func(self.preview_display.copy())
                self.preview_display = _ensure_bgr_uint8(new_preview)
                self._preview_chain.append(preview_func)
                self._full_chain.append(full_func)
            else:
                new_preview = preview_func(self.base_display.copy())
                self.preview_display = _ensure_bgr_uint8(new_preview)
                self._preview_chain = [preview_func]
                self._full_chain = [full_func]
            self._update_preview_widget(preview_label)
        except Exception as e:
            warnings.warn(f"Preview filter '{name}' failed: {e}", RuntimeWarning)
            self._show_error(f"Preview of filter '{name}' failed:\n{e}")

    def _on_reset(self, preview_label: ttk.Label):
        self._full_chain = []
        self._preview_chain = []
        self.preview_display = self.base_display.copy()
        self._update_preview_widget(preview_label)

    def _on_apply(self):
        out = self.base_full.copy()
        try:
            for f in self._full_chain:
                out = f(out)
            out = _ensure_bgr_uint8(out)
        except Exception as e:
            warnings.warn(f"Full apply failed: {e}", RuntimeWarning)
            self._show_error(f"Applying filters to full image failed:\n{e}")
            return
        self._result = out
        if self.top:
            self.top.destroy()

    def _on_cancel(self):
        self._result = None
        if self.top:
            self.top.destroy()

    def _show_error(self, message: str):
        err = tk.Toplevel(self.top or self.parent)
        err.title("Error")
        tk.Label(err, text=message, padx=10, pady=8, wraplength=420, justify="left").pack()
        tk.Button(err, text="OK", command=err.destroy).pack(pady=6)
        err.transient(self.top or self.parent)
        err.grab_set()
        (self.parent or self.top).wait_window(err)

    # ---- public API ----
    def run(self) -> Optional[ArrayLike]:
        """
        Launch the modal popup. Returns processed full-resolution BGR image or None if cancelled.
        """
        if self.parent is None:
            raise ValueError("parent tk window is required")

        self.top = tk.Toplevel(self.parent)
        self.top.title(self.title)
        self.top.resizable(self.resizable, self.resizable)

        # Left: filter buttons
        left = ttk.Frame(self.top)
        left.grid(row=0, column=0, padx=8, pady=8, sticky="n")

        ttk.Label(left, text="Filters", font=("TkDefaultFont", 10, "bold")).pack(pady=(0, 6))
        for name, full_f, preview_f in self._filters:
            btn = ttk.Button(
                left,
                text=name,
                width=self.button_width,
                command=lambda ff=full_f, pf=preview_f, nm=name: self._on_filter_click(ff, pf, nm, preview_label),
            )
            btn.pack(pady=2)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=6)
        ttk.Button(left, text="Reset", width=self.button_width, command=lambda: self._on_reset(preview_label)).pack(pady=3)
        ttk.Button(left, text="Apply", width=self.button_width, command=self._on_apply).pack(pady=3)
        ttk.Button(left, text="Cancel", width=self.button_width, command=self._on_cancel).pack(pady=3)

        # Middle: base and preview
        mid = ttk.Frame(self.top)
        mid.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(mid, text="Base (unchanged)").pack()
        base_label = ttk.Label(mid)
        base_label.pack(padx=4, pady=4)

        ttk.Label(mid, text="Preview").pack(pady=(8, 0))
        preview_label = ttk.Label(mid)
        preview_label.pack(padx=4, pady=4)

        # initialize images
        self._update_base_widget(base_label)
        self._update_preview_widget(preview_label)

        # modal behavior
        self.top.transient(self.parent)
        self.top.grab_set()
        self.parent.wait_window(self.top)

        return self._result


# -------------------- Convenience one-liner --------------------
def show_filter_session(parent, image_bgr: ArrayLike, filters: Sequence[FilterDescriptor], **kwargs) -> Optional[ArrayLike]:
    """
    Quick helper: show popup with given filters and image and return processed image.
    kwargs forwarded to FilterSession constructor (display_max_size, cumulative, title, ...).
    """
    sess = FilterSession(parent, filters, image_bgr, **kwargs)
    return sess.run()


# Exports
__all__ = ["FilterSession", "show_filter_session"]
