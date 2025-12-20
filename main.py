import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import time
import matplotlib.pyplot as plt

from pages.Smooth import Smooth
from pages.Sharp import Sharp
from pages.Noise import Noise

img_path = None


def select_image():
    global img_path, img_label, img_tk
    img_path = filedialog.askopenfilename(
        title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if img_path:
        img_pil = Image.open(img_path)
        img_pil.thumbnail((400, 300))
        img_tk = ImageTk.PhotoImage(img_pil)
        img_label.config(image=img_tk)
        img_label.image = img_tk
        messagebox.showinfo(
            "Image Selected", f"Selected image: {os.path.basename(img_path)}"
        )


def cv2_run():
    im2 = cv2.imread(img_path)
    cv2.imshow("Original Image", im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Smooth_run(root):
    
    Smooth(root, cv2.imread(img_path))


def Sharp_run(root):
    Sharp(root, cv2.imread(img_path))


def Noise_run(root):
    Noise(root, cv2.imread(img_path))


root = tk.Tk()
root.title("Image Processing Application")
root.geometry("800x600")
root.resizable(False, False)

# Configure grid weights for proper resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

img_pil = Image.new("RGB", (400, 300), color="gray")
img_def = Image.new("RGB", (400, 300), color="gray")
img_tk = ImageTk.PhotoImage(img_pil)
img_label = ttk.Label(root, image=img_tk)
img_label.image = img_tk
img_label.grid(row=0, column=0, columnspan=3, pady=20)

img_btn = ttk.Button(root, text="Select Image", command=select_image)
img_btn.grid(row=1, column=0, pady=10, padx=5)

run_btn = ttk.Button(root, text="Run CV2", command=cv2_run)
run_btn.grid(row=1, column=1, pady=10, padx=5)

clr_btn = ttk.Button(root, text="Clear Image", command=lambda: img_label.config(image=ImageTk.PhotoImage(img_def)))
clr_btn.grid(row=1, column=2, pady=10, padx=5)

filter_lbl = ttk.Label(root, text="Select Filter:",font=("Arial", 20, "bold"))
filter_lbl.grid(row=2, column=0, pady=10, padx=5,columnspan=3)

smooth_btn = ttk.Button(root, text="Smooth", command=lambda: Smooth_run(root))
smooth_btn.grid(row=3, column=0, pady=10, padx=1)

sharp_btn = ttk.Button(root, text="Sharp", command=lambda: Sharp_run(root))
sharp_btn.grid(row=3, column=1, pady=10, padx=1)

noise_btn = ttk.Button(root, text="Noise", command=lambda: Noise_run(root))
noise_btn.grid(row=3, column=2, pady=10, padx=1)
root.mainloop()
