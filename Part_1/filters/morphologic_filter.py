import math
import cv2
import numpy as np

"""
parameters : 
    kernel_size : odd numbers only.
    kernel_shape : 'rect', 'cross', 'ellipse'.
    iterations : optional, by default 1.
"""

# ------------------ Dilation
def dilation(img, kernel_size, kernel_shape, iterations):
    # Creating the kernel matrix 
    if kernel_shape == "rect":
        kernel_list = [[1 for i in range(kernel_size)] for j in range(kernel_size)]
        kernel = np.array(kernel_list)
    elif kernel_shape == "cross":
        kernel_list = [
            [
                1 if i == kernel_size // 2 or j == kernel_size // 2 else 0
                for i in range(kernel_size)
            ]
            for j in range(kernel_size)
        ]
        kernel = np.array(kernel_list)
    elif kernel_shape == "ellipse":
        kernel = np.zeros((kernel_size, kernel_size), dtype=np.uint8)
        center = (kernel_size - 1) / 2
        radius = center
        for i in range(kernel_size):
            for j in range(kernel_size):
                if ((i - center) / radius) ** 2 + ((j - center) / radius) ** 2 <= 1:
                    kernel[i, j] = 1

    # Creating an image having the same shape as the input image
    height, width = img.shape
    img_result = np.zeros((height, width))

    # For each iteration 
    for iteration in range(iterations):
        # For each pixel
        for i in range( height ) :
            for j in range( width ) :

                # Check if the pixel is not a black one, if yes we perform the dilation operation
                if img[i, j] > 0:

                    # For each point in the kernel
                    for h in range( kernel_size ) :
                        for w in range( kernel_size ) :

                            # If this point is a One (exclude points in kernel where equal to 0)
                            if kernel[h, w] == 1:
                                # Get the boundaries of the kernel when applied to the pixel img[i, j]
                                row = i - kernel_size // 2 + h
                                col = j - kernel_size // 2 + w
                                # If row is out of bounds or col is out of bounds : continue. else : perform the dilation
                                if height > row >= 0 and width > col >= 0:
                                    # Dilate the region by assigning the the neighors of the pixel by the max value : 255
                                    img_result[row, col] = 255

        # If more iterations : so affect img_result to img, so we can rework on the new image
        img = img_result.copy()

    return img_result


# ------------------ Erosion
def erosion(img, kernel_size, kernel_shape, iterations):
    # Creating the kernel matrix 
    if kernel_shape == "rect":
        kernel_list = [[1 for i in range(kernel_size)] for j in range(kernel_size)]
        kernel = np.array(kernel_list)
    elif kernel_shape == "cross":
        kernel_list = [
            [
                1 if i == kernel_size // 2 or j == kernel_size // 2 else 0
                for i in range(kernel_size)
            ]
            for j in range(kernel_size)
        ]
        kernel = np.array(kernel_list)
    elif kernel_shape == "ellipse":
        kernel = np.zeros((kernel_size, kernel_size), dtype=np.uint8)
        center = (kernel_size - 1) / 2
        radius = center
        for i in range(kernel_size):
            for j in range(kernel_size):
                if ((i - center) / radius) ** 2 + ((j - center) / radius) ** 2 <= 1:
                    kernel[i, j] = 1

    # Creating an image having the same shape as the input image
    height, width = img.shape
    img_result = np.zeros((height, width))

    # For each iteration 
    for iteration in range(iterations):

        # For each pixel 
        for i in range( height ) :
            for j in range( width ) :

                # Check if the pixel is not a black one, if yes we perform the erosion operation
                if img[i, j] > 0:
                    # Boolean all_pixels_are_one to check if the covered region by kernel doesn't contain black pixels
                    all_pixels_are_one = True

                    # For each point in the kernel
                    for h in range( kernel_size ) :
                        for w in range( kernel_size ) :

                            # If this point is a One (exclude points in kernel where equal to 0)
                            if kernel[h, w] == 1:
                                # Get the boundaries of the kernel when applied to the pixel img[i, j]
                                row = i - kernel_size // 2 + h
                                col = j - kernel_size // 2 + w
                                # If row is out of bounds or col is out of bounds : continue. else : perform the erosion
                                if height > row >= 0 and width > col >= 0:
                                    # If there is just one pixel black in the region of pixel img[i,j], boolean all_pixels_are_one will be False,
                                    # and we break process for this line in kernel
                                    if img[row, col] == 0:
                                        all_pixels_are_one = False
                                        break

                        # If all_pixels_are_one == False, means there is a black pixel in the previous line, 
                        # so, we break process for the entire kernel
                        if not all_pixels_are_one:
                            break

                    # If all_pixels_are_one == True, means the kernel covered the region of pixel img[i,j]
                    # so, we save the pixel, else : we keep it 0
                    if all_pixels_are_one:
                        img_result[i, j] = 255

        # If more iterations : so affect img_result to img, so we can rework on the new image
        img = img_result.copy()
        
    return img_result


# ------------------ Opening
def opening(img, kernel_size, kernel_shape, iterations):
    return dilation(
        erosion(img, kernel_size, kernel_shape, iterations=1),
        kernel_size,
        kernel_shape,
        iterations,
    )


# ------------------ Closing
def closing(img, kernel_size, kernel_shape, iterations):
    return erosion(
        dilation(img, kernel_size, kernel_shape, iterations=1),
        kernel_size,
        kernel_shape,
        iterations,
    )







