import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import sys
import os

# sys.path.insert(0, r"C:\\Users\\HI\\My-Github\\Computer_Vision_Project")

# Get the project's root directory
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project's root directory to sys.path
sys.path.insert(0, project_directory)

from Part_1.filters.bilateral_filter import bilateral_filter
from Part_1.filters.Gaussian_filter import gaussian_filter
from Part_1.filters.laplacian_filter import laplacian_filter
from Part_1.filters.mean_filter import mean_filter
from Part_1.filters.median_filter import median_filter
from Part_1.filters.morphologic_filter import erosion, dilation, opening, closing
from Part_1.filters.sobel_filter import sobel_filter
from Part_1.filters.threshold_filter import custom_threshold

from Part_1.invisibility_cloak import invisibility_cloak
from Part_1.object_detection import ObjectDetector
from Part_1.green_screen import GreenScreen
from Part_2.game import Game


# import Part_1.object_detection


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


def apply_filter(
    image,
    filter,
    kernel_size=None,
    kernel_shape=None,
    iterations=None,
    vois=None,
    spatial_sigma=None,
    intensity_sigma=None,
    threshold=None,
    threshold_type=None,
):
    image = cv2.resize(
        image, (canvas_width, canvas_height), interpolation=cv2.INTER_AREA
    )

    if filter in {gaussian_filter, laplacian_filter, sobel_filter}:
        img_filtered = filter(image)
    elif filter in {mean_filter, median_filter}:
        img_filtered = filter(image, vois)
    elif filter in {erosion, dilation, opening, closing}:
        img_filtered = filter(image, kernel_size, kernel_shape, iterations)
    elif filter == bilateral_filter:
        img_filtered = filter(image, vois, spatial_sigma, intensity_sigma)
    elif filter == custom_threshold:
        img_filtered = filter(image, threshold, threshold_type)
    else:
        raise ValueError(f"Unsupported filter: {filter}")

    # img_filtered_resized = cv2.resize(
    #     img_filtered, (canvas_width, canvas_height), interpolation=cv2.INTER_AREA
    # )
    img_filtered_tk = ImageTk.PhotoImage(Image.fromarray(img_filtered))
    canvas2.config(width=canvas_width, height=canvas_height)
    canvas2.create_image(0, 0, anchor="nw", image=img_filtered_tk)
    canvas2.image = img_filtered_tk


def on_entry_click(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")  # Delete the default placeholder text
        entry.insert(0, "")  # Set the text color to black


def on_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)  # If no text was entered, set placeholder back
        entry.config(fg="grey")  # Set the text color to grey


root = tk.Tk()
root.title("Computer Vision Project")

left_frame = Frame(root)
left_frame.pack(side=LEFT)

right_frame = Frame(root)
right_frame.pack(side=LEFT, expand=True, fill="both", padx=10, pady=10)

# Define the canvas size
canvas_width = 250
canvas_height = 250

root_color = root.cget("bg")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background=root_color)
style.configure("TLabel", padding=6, background=root_color)
style.configure("TEntry", padding=6, relief="flat", background="white")

optionmenu_style = ttk.Style()
optionmenu_style.configure("TMenubutton", padding=(10, 6), relief="flat")

canvas1 = tk.Canvas(left_frame, width=canvas_width, height=canvas_height, bg=root_color)
canvas1.grid(row=0, column=1, padx=40, pady=10, rowspan=2)

canvas2 = tk.Canvas(left_frame, width=canvas_width, height=canvas_height, bg=root_color)
canvas2.grid(row=2, column=1, padx=40, pady=10, rowspan=2)


# Load and resize the image to fit the canvas
# img_path = r"C:\\Users\\HI\\My-Github\\Computer_Vision_Project\\GUI\\img.jpg"
img_path = os.path.join(project_directory, 'GUI', 'img.jpg')

img_size = (canvas_width, canvas_height)
img = load_and_resize_image(img_path, img_size)

image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Create an image on canvas1
canvas1.create_image(0, 0, anchor="nw", image=img)

label = ttk.Label(right_frame, text="Filters", font=("Helvetica", 16))
label.grid(row=0, column=0, padx=10, pady=10)

# ------------------------------------------
# Filters' Buttons
# ------------------------------------------

button1 = ttk.Button(
    right_frame,
    text="Gaussian",
    width=15,
    command=lambda: apply_filter(np.array(image), gaussian_filter),
).grid(row=1, column=0, padx=10, pady=10)

button2 = ttk.Button(
    right_frame,
    text="Laplacian",
    width=15,
    command=lambda: apply_filter(np.array(image), laplacian_filter),
).grid(row=1, column=1, padx=10, pady=10)

button3 = ttk.Button(
    right_frame,
    text="Sobel",
    width=15,
    command=lambda: apply_filter(np.array(image), sobel_filter),
).grid(row=1, column=2, padx=10, pady=10)


mean_vois = tk.Entry(right_frame, width=15)
mean_vois.grid(row=4, column=1, padx=10, pady=10)
mean_vois.insert(0, "Neighbors")  # Set a placeholder
mean_vois.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
mean_vois.bind("<FocusIn>", lambda event, e=mean_vois: on_entry_click(e, "Neighbors"))
mean_vois.bind("<FocusOut>", lambda event, e=mean_vois: on_focus_out(e, "Neighbors"))

button4 = ttk.Button(
    right_frame,
    text="Mean",
    width=15,
    command=lambda: apply_filter(
        np.array(image), mean_filter, vois=int(mean_vois.get())
    ),
).grid(row=4, column=0, padx=10, pady=10)

median_vois = tk.Entry(right_frame, width=15)
median_vois.grid(row=5, column=1, padx=10, pady=10)
median_vois.insert(0, "Neighbors")  # Set a placeholder
median_vois.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
median_vois.bind(
    "<FocusIn>", lambda event, e=median_vois: on_entry_click(e, "Neighbors")
)
median_vois.bind(
    "<FocusOut>", lambda event, e=median_vois: on_focus_out(e, "Neighbors")
)

button5 = ttk.Button(
    right_frame,
    text="Median",
    width=15,
    command=lambda: apply_filter(
        np.array(image), median_filter, vois=int(median_vois.get())
    ),
)
button5.grid(row=5, column=0, padx=10, pady=10)

erosion_kernel_size = tk.Entry(right_frame, width=15)
erosion_kernel_size.grid(row=6, column=1, padx=10, pady=10)
erosion_kernel_size.insert(0, "Kernel size")  # Set a placeholder
erosion_kernel_size.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
erosion_kernel_size.bind(
    "<FocusIn>", lambda event, e=erosion_kernel_size: on_entry_click(e, "Kernel size")
)
erosion_kernel_size.bind(
    "<FocusOut>", lambda event, e=erosion_kernel_size: on_focus_out(e, "Kernel size")
)

erosion_iterations = tk.Entry(right_frame, width=15)
erosion_iterations.grid(row=6, column=2, padx=10, pady=10)
erosion_iterations.insert(0, "Iterations")  # Set a placeholder
erosion_iterations.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
erosion_iterations.bind(
    "<FocusIn>", lambda event, e=erosion_iterations: on_entry_click(e, "Iterations")
)
erosion_iterations.bind(
    "<FocusOut>", lambda event, e=erosion_iterations: on_focus_out(e, "Iterations")
)

erosion_kernel_shape = ["rect", "cross", "ellipse"]
# Create a StringVar to store the selected threshold type
selected_ero_shape = StringVar()
selected_ero_shape.set(erosion_kernel_shape[0])  # Set the default value
# Create an OptionMenu with the styled theme
ero_shape = ttk.OptionMenu(right_frame, selected_ero_shape, *erosion_kernel_shape)
ero_shape.grid(row=6, column=3, padx=10, pady=10)

# Set the background color for the OptionMenu
ero_shape["menu"].config(bg="white")

button6 = ttk.Button(
    right_frame,
    text="Erosion",
    width=15,
    command=lambda: apply_filter(
        np.array(image),
        erosion,
        kernel_size=int(erosion_kernel_size.get()),
        kernel_shape=selected_ero_shape.get(),
        iterations=int(erosion_iterations.get()),
    ),
)
button6.grid(row=6, column=0, padx=10, pady=10)

dilation_kernel_size = tk.Entry(right_frame, width=15)
dilation_kernel_size.grid(row=7, column=1, padx=10, pady=10)
dilation_kernel_size.insert(0, "Kernel size")  # Set a placeholder
dilation_kernel_size.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
dilation_kernel_size.bind(
    "<FocusIn>", lambda event, e=dilation_kernel_size: on_entry_click(e, "Kernel size")
)
dilation_kernel_size.bind(
    "<FocusOut>", lambda event, e=dilation_kernel_size: on_focus_out(e, "Kernel size")
)

dilation_iterations = tk.Entry(right_frame, width=15)
dilation_iterations.grid(row=7, column=2, padx=10, pady=10)
dilation_iterations.insert(0, "Iterations")  # Set a placeholder
dilation_iterations.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
dilation_iterations.bind(
    "<FocusIn>", lambda event, e=dilation_iterations: on_entry_click(e, "Iterations")
)
dilation_iterations.bind(
    "<FocusOut>", lambda event, e=dilation_iterations: on_focus_out(e, "Iterations")
)

dilation_kernel_shape = ["rect", "cross", "ellipse"]
# Create a StringVar to store the selected threshold type
selected_dilo_shape = StringVar()
selected_dilo_shape.set(dilation_kernel_shape[0])  # Set the default value
# Create an ttk.OptionMenu with the threshold types
dilo_shape = ttk.OptionMenu(right_frame, selected_dilo_shape, *dilation_kernel_shape)
dilo_shape.grid(row=7, column=3, padx=10, pady=10)
dilo_shape["menu"].config(bg="white")


button7 = ttk.Button(
    right_frame,
    text="Dilation",
    width=15,
    command=lambda: apply_filter(
        np.array(image),
        dilation,
        kernel_size=int(dilation_kernel_size.get()),
        kernel_shape=selected_dilo_shape.get(),
        iterations=int(dilation_iterations.get()),
    ),
)
button7.grid(row=7, column=0, padx=10, pady=10)

opening_kernel_size = tk.Entry(right_frame, width=15)
opening_kernel_size.grid(row=8, column=1, padx=10, pady=10)
opening_kernel_size.insert(0, "Kernel size")  # Set a placeholder
opening_kernel_size.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
opening_kernel_size.bind(
    "<FocusIn>", lambda event, e=opening_kernel_size: on_entry_click(e, "Kernel size")
)
opening_kernel_size.bind(
    "<FocusOut>", lambda event, e=opening_kernel_size: on_focus_out(e, "Kernel size")
)

opening_iterations = tk.Entry(right_frame, width=15)
opening_iterations.grid(row=8, column=2, padx=10, pady=10)
opening_iterations.insert(0, "Iterations")  # Set a placeholder
opening_iterations.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
opening_iterations.bind(
    "<FocusIn>", lambda event, e=opening_iterations: on_entry_click(e, "Iterations")
)
opening_iterations.bind(
    "<FocusOut>", lambda event, e=opening_iterations: on_focus_out(e, "Iterations")
)

opening_kernel_shape = ["rect", "cross", "ellipse"]
# Create a StringVar to store the selected threshold type
selected_open_shape = StringVar()
selected_open_shape.set(opening_kernel_shape[0])
# Create an ttk.OptionMenu with the threshold types
open_shape = ttk.OptionMenu(right_frame, selected_open_shape, *opening_kernel_shape)
open_shape.grid(row=8, column=3, padx=10, pady=10)
open_shape["menu"].config(bg="white")

button8 = ttk.Button(
    right_frame,
    text="Opening",
    width=15,
    command=lambda: apply_filter(
        np.array(image),
        opening,
        kernel_size=int(opening_kernel_size.get()),
        kernel_shape=selected_open_shape.get(),
        iterations=int(opening_iterations.get()),
    ),
)
button8.grid(row=8, column=0, padx=10, pady=10)

closing_kernel_size = tk.Entry(right_frame, width=15)
closing_kernel_size.grid(row=9, column=1, padx=10, pady=10)
closing_kernel_size.insert(0, "Kernel size")  # Set a placeholder
closing_kernel_size.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
closing_kernel_size.bind(
    "<FocusIn>", lambda event, e=closing_kernel_size: on_entry_click(e, "Kernel size")
)
closing_kernel_size.bind(
    "<FocusOut>", lambda event, e=closing_kernel_size: on_focus_out(e, "Kernel size")
)

closing_iterations = tk.Entry(right_frame, width=15)
closing_iterations.grid(row=9, column=2, padx=10, pady=10)
closing_iterations.insert(0, "Iterations")  # Set a placeholder
closing_iterations.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
closing_iterations.bind(
    "<FocusIn>", lambda event, e=closing_iterations: on_entry_click(e, "Iterations")
)
closing_iterations.bind(
    "<FocusOut>", lambda event, e=closing_iterations: on_focus_out(e, "Iterations")
)

closing_kernel_shape = ["rect", "cross", "ellipse"]
# Create a StringVar to store the selected threshold type
selected_close_shape = StringVar()
selected_close_shape.set(closing_kernel_shape[0])  # Set the default value
# Create an ttk.OptionMenu with the threshold types
close_shape = ttk.OptionMenu(right_frame, selected_close_shape, *closing_kernel_shape)
close_shape.grid(row=9, column=3, padx=10, pady=10)
close_shape["menu"].config(bg="white")


button9 = ttk.Button(
    right_frame,
    text="Closing",
    width=15,
    command=lambda: apply_filter(
        np.array(image),
        closing,
        kernel_size=int(closing_kernel_size.get()),
        kernel_shape=selected_close_shape.get(),
        iterations=int(closing_iterations.get()),
    ),
)
button9.grid(row=9, column=0, padx=10, pady=10)

bilateral_vois = tk.Entry(right_frame, width=15)
bilateral_vois.grid(row=10, column=1, padx=10, pady=10)
bilateral_vois.insert(0, "Neighbors")  # Set a placeholder
bilateral_vois.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
bilateral_vois.bind(
    "<FocusIn>", lambda event, e=bilateral_vois: on_entry_click(e, "Neighbors")
)
bilateral_vois.bind(
    "<FocusOut>", lambda event, e=bilateral_vois: on_focus_out(e, "Neighbors")
)

spatial_sigma = tk.Entry(right_frame, width=15)
spatial_sigma.grid(row=10, column=2, padx=10, pady=10)
spatial_sigma.insert(0, "Spatial Sigma")  # Set a placeholder
spatial_sigma.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
spatial_sigma.bind(
    "<FocusIn>", lambda event, e=spatial_sigma: on_entry_click(e, "Spatial Sigma")
)
spatial_sigma.bind(
    "<FocusOut>", lambda event, e=spatial_sigma: on_focus_out(e, "Spatial Sigma")
)

intensity_sigma = tk.Entry(right_frame, width=15)
intensity_sigma.grid(row=10, column=3, padx=10, pady=10)
intensity_sigma.insert(0, "Intensity Sigma")  # Set a placeholder
intensity_sigma.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
intensity_sigma.bind(
    "<FocusIn>", lambda event, e=intensity_sigma: on_entry_click(e, "Intensity Sigma")
)
intensity_sigma.bind(
    "<FocusOut>", lambda event, e=intensity_sigma: on_focus_out(e, "Intensity Sigma")
)


button10 = ttk.Button(
    right_frame,
    text="Bilateral",
    width=15,
    command=lambda: apply_filter(
        np.array(image),
        bilateral_filter,
        vois=int(bilateral_vois.get()),
        spatial_sigma=int(spatial_sigma.get()),
        intensity_sigma=int(intensity_sigma.get()),
    ),
)
button10.grid(row=10, column=0, padx=10, pady=10)


threshold = tk.Entry(right_frame, width=15)
threshold.grid(row=11, column=1, padx=10, pady=10)
threshold.insert(0, "Threshold")  # Set a placeholder
threshold.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
threshold.bind("<FocusIn>", lambda event, e=threshold: on_entry_click(e, "Threshold"))
threshold.bind("<FocusOut>", lambda event, e=threshold: on_focus_out(e, "Threshold"))


threshold_types = ["binary", "binary_inv", "trunc", "tozero", "tozero_inv"]
# Create a StringVar to store the selected threshold type
selected_threshold_type = StringVar()
selected_threshold_type.set(threshold_types[0])  # Set the default value
# Create an ttk.OptionMenu with the threshold types
thre_type = ttk.OptionMenu(right_frame, selected_threshold_type, *threshold_types)
thre_type.grid(row=11, column=2, padx=10, pady=10)

button11 = ttk.Button(
    right_frame,
    text="Threshold",
    width=15,
    command=lambda: apply_filter(
        np.array(image),
        custom_threshold,
        threshold=int(threshold.get()),
        threshold_type=selected_threshold_type.get(),  # Use the selected threshold type
    ),
)
button11.grid(row=11, column=0, padx=10, pady=10)

# ------------------------------------------
# Functions' Buttons
# ------------------------------------------


def run_object_detection():
    object_detection = ObjectDetector()
    object_detection.run()


button12 = ttk.Button(
    right_frame,
    text="Object Detection",
    width=15,
    command=lambda: run_object_detection(),
)
button12.grid(row=12, column=0, padx=10, pady=10)


# def run_green_screen():
#     green_screen = GreenScreen(
#         r"C:\Users\HI\My-Github\Computer_Vision_Project\back.jpg"
#     )
#     green_screen.run()

def run_green_screen():
    img_path = os.path.join(project_directory, 'back.jpg')
    green_screen = GreenScreen(img_path)
    green_screen.run()



button13 = ttk.Button(
    right_frame, text="Green Screen", width=15, command=lambda: run_green_screen()
)
button13.grid(row=12, column=1, padx=10, pady=10)


def run_invisibility_cloak():
    cloak_instance = invisibility_cloak()
    cloak_instance.run()


button13 = ttk.Button(
    right_frame,
    text="Invisibility Cloak",
    width=15,
    command=lambda: run_invisibility_cloak(),
)
button13.grid(row=12, column=2, padx=10, pady=10)


def run_game():
    game = Game(360, 540)
    game.run()


button12 = ttk.Button(
    right_frame, text="Brick Race Game", width=15, command=lambda: run_game()
)
button12.grid(row=13, column=1, padx=10, pady=10)


window_width = 970
window_height = 750
root.geometry(f"{window_width}x{window_height}")

root.mainloop()
