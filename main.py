import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import cv2
from PIL import Image, ImageTk

from pages.Smooth import Smooth
from pages.Sharp import Sharp
from pages.Noise import Noise

img_path = None
out = None
org = None


def read_image():
    global img_path, img_label, img_tk
    if img_path:
        img_pil = Image.open(img_path)
        img_pil.thumbnail((400, 300))
        img_tk = ImageTk.PhotoImage(img_pil)
        img_label.config(image=img_tk)
        img_label.image = img_tk


def reset_image():
    global img_path, img_label, img_tk, org
    if org:
        img_path = org
        read_image()
        messagebox.showinfo("Reset", "Image reset to original")


def clear_image():
    global img_path, img_label, img_tk, org
    img_def = Image.new("RGB", (400, 300), color="gray")
    img_tk = ImageTk.PhotoImage(img_def)
    img_label.config(image=img_tk)
    img_label.image = img_tk
    messagebox.showinfo("Image Cleared","Image Cleared Successfully")


def select_image():
    global img_path, img_label, img_tk, org
    img_path = filedialog.askopenfilename(
        title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    org = img_path
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
    global out, img_path
    out = Smooth(root, cv2.imread(img_path))
    cv2.imwrite("output.png", out)
    img_path = "output.png"
    read_image()


def Sharp_run(root):
    global out, img_path
    out = Sharp(root, cv2.imread(img_path))
    cv2.imwrite("output.png", out)
    img_path = "output.png"
    read_image()


def Noise_run(root):
    global out, img_path
    out = Noise(root, cv2.imread(img_path))
    cv2.imwrite("output.png", out)
    img_path = "output.png"
    read_image()


root = tk.Tk()
root.title("Image Processing Application")
root.geometry("800x600")
root.resizable(False, False)
root.config(bg="#303031")


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

img_pil = Image.new("RGB", (400, 300), color="gray")
img_def = Image.new("RGB", (400, 300), color="gray")
img_tk = ImageTk.PhotoImage(img_pil)
img_label = tk.Label(root, image=img_tk)
img_label.image = img_tk
img_label.grid(row=0, column=0, columnspan=3, pady=20)

img_btn = tk.Button(
    root,
    text="Select Image",
    command=select_image,
    font=("Arial", 10, "bold"),
    border=2,
    bg="#1F5579",
    fg="white",
)
img_btn.grid(row=1, column=0, pady=10, padx=5)

run_btn = tk.Button(
    root,
    text="Reset Image",
    command=reset_image,
    font=("Arial", 10, "bold"),
    border=2,
    bg="#000000",
    fg="white",
)
run_btn.grid(row=1, column=1, pady=10, padx=5)

clr_btn = tk.Button(
    root,
    text="Clear Image",
    command=clear_image,
    font=("Arial", 10, "bold"),
    border=2,
    bg="#992525",
    fg="white",
)
clr_btn.grid(row=1, column=2, pady=10, padx=5)

filter_lbl = tk.Label(
    root, text="Select Filter:", font=("Arial", 20, "bold"), bg="#303031", fg="white"
)
filter_lbl.grid(row=2, column=0, pady=10, padx=5, columnspan=3)

smooth_btn = tk.Button(
    root,
    text="Smooth",
    command=lambda: Smooth_run(root),
    font=("Arial", 10, "bold"),
    border=2,
    bg="#00AE17",
    fg="white",
)
smooth_btn.grid(row=3, column=0, pady=10, padx=1)

sharp_btn = tk.Button(
    root,
    text="Sharp",
    command=lambda: Sharp_run(root),
    font=("Arial", 10, "bold"),
    border=2,
    bg="#00AE17",
    fg="white",
)
sharp_btn.grid(row=3, column=1, pady=10, padx=1)

noise_btn = tk.Button(
    root,
    text="Noise",
    command=lambda: Noise_run(root),
    font=("Arial", 10, "bold"),
    border=2,
    bg="#00AE17",
    fg="white",
)
noise_btn.grid(row=3, column=2, pady=10, padx=1)
root.mainloop()
