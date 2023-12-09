import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import sys

sys.path.insert(0, r"C:\\Users\\HI\\My-Github\\Computer_Vision_Project")
from Part_1.filters.bilateral_filter import bilateral_filter
from Part_1.filters.Gaussian_filter import gaussian_filter
from Part_1.filters.laplacian_filter import laplacian_filter
from Part_1.filters.mean_filter import mean_filter
from Part_1.filters.median_filter import median_filter
from Part_1.filters.morphologic_filter import erosion, dilation
from Part_1.filters.sobel_filter import sobel_filter


def load_and_resize_image(path, size):
    # Try to read the image
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was successfully loaded
    if image is None:
        print(f"Error: Unable to read image from {path}")
        return None

    # Resize the image
    resized_image = cv2.resize(image, (size[1], size[0]), interpolation=cv2.INTER_AREA)

    return ImageTk.PhotoImage(Image.fromarray(resized_image))


def apply_filter(image, filter):
    img_filtered = filter(image)
    img_filtered_resized = cv2.resize(
        img_filtered, (canvas_width, canvas_height), interpolation=cv2.INTER_AREA
    )
    img_filtered_tk = ImageTk.PhotoImage(Image.fromarray(img_filtered_resized))
    canvas2.config(width=canvas_width, height=canvas_height)
    canvas2.create_image(0, 0, anchor="nw", image=img_filtered_tk)
    canvas2.image = img_filtered_tk


root = tk.Tk()
root.title("Computer Vision Project")

left_frame = Frame(root)
left_frame.pack(side=LEFT)

right_frame = Frame(root, bg="red")
right_frame.pack(side=RIGHT)

# Define the canvas size
canvas_width = 250
canvas_height = 250

canvas1 = tk.Canvas(left_frame, width=canvas_width, height=canvas_height, bg="white")
canvas1.grid(row=0, column=1, padx=40, pady=10, rowspan=2)

canvas2 = tk.Canvas(left_frame, width=canvas_width, height=canvas_height, bg="white")
canvas2.grid(row=2, column=1, padx=40, pady=10, rowspan=2)


# Load and resize the image to fit the canvas
img_path = r"C:\\Users\\HI\\My-Github\\Computer_Vision_Project\\GUI\\img.jpg"
img_size = (canvas_width, canvas_height)
img = load_and_resize_image(img_path, img_size)

image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Create an image on canvas1
canvas1.create_image(0, 0, anchor="nw", image=img)

label = tk.Label(right_frame, text="Filters", font=("Helvetica", 16))
label.grid(row=0, column=0, padx=10, pady=10)

# Buttons
# button1 = tk.Button(
#     right_frame,
#     text="Mean",
#     width=15,
#     command=lambda: apply_filter(np.array(image), mean_filter),
# )
# button1.grid(row=0, column=2, padx=10, pady=10)


# button2 = tk.Button(
#     right_frame,
#     text="Median",
#     width=15,
#     command=lambda: apply_filter(np.array(image), median_filter),
# )
# button2.grid(row=0, column=3, padx=10, pady=10)

button4 = tk.Button(
    right_frame,
    text="Gaussian",
    width=15,
    command=lambda: apply_filter(np.array(image), gaussian_filter),
)
button4.grid(row=0, column=1, padx=10, pady=10)

button3 = tk.Button(
    right_frame,
    text="Laplacian",
    width=15,
    command=lambda: apply_filter(np.array(image), laplacian_filter),
)
button3.grid(row=0, column=1, padx=10, pady=10)

# button5 = tk.Button(
#     right_frame,
#     text="Morphologie",
#     width=15,
#     command=lambda: apply_filter(np.array(image), morphologic_filter),
# )
# button5.grid(row=1, column=3, padx=10, pady=10)

# button6 = tk.Button(
#     right_frame,
#     text="Bilateral",
#     width=15,
#     command=lambda: apply_filter(np.array(image), bilateral_filter),
# )
# button6.grid(row=1, column=4, padx=10, pady=10)

button7 = tk.Button(
    right_frame,
    text="Sobel",
    width=15,
    command=lambda: apply_filter(np.array(image), sobel_filter),
)
button7.grid(row=2, column=3, padx=10, pady=10)

# button8 = tk.Button(
#     right_frame,
#     text="Object Detection",
#     width=15,
#     command=,
# )
# button8.grid(row=2, column=3, padx=10, pady=10)

window_width = 800
window_height = 600
root.geometry(f"{window_width}x{window_height}")

root.mainloop()
