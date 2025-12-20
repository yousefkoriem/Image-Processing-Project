import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import time
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("Image Processing Application")
root.geometry("800x600")
root.resizable(False, False)
root.mainloop()