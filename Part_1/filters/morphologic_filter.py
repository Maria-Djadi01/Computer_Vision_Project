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

    height, width = img.shape
    img_result = np.zeros((height, width))

    for iteration in range(iterations):
        
        for i in range( height ) :
            for j in range( width ) :
                
                if img[i, j] > 0:
            
                    for h in range( kernel_size ) :
                        for w in range( kernel_size ) :
                            
                            if kernel[h, w] == 1:
                                row = i - kernel_size // 2 + h
                                col = j - kernel_size // 2 + w
                                if height > row >= 0 and width > col >= 0:
                                    img_result[row, col] = img[i,j]

        img = img_result.copy()

    return img_result


# ------------------ Erosion
def erosion(img, kernel_size, kernel_shape, iterations):
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

    height, width = img.shape
    img_result = np.zeros((height, width))

    for iteration in range(iterations):
        
        for i in range( height ) :
            for j in range( width ) :
                
                if img[i, j] > 0:
                    all_pixels_are_one = True
                    
                    for h in range( kernel_size ) :
                        for w in range( kernel_size ) :
                            
                            if kernel[h, w] == 1:
                                row = i - kernel_size // 2 + h
                                col = j - kernel_size // 2 + w
                                if height > row >= 0 and width > col >= 0:
                                    if img[row, col] == 0:
                                        all_pixels_are_one = False
                                        break

                        if not all_pixels_are_one:
                            break

                    if all_pixels_are_one:
                        img_result[i, j] = img[i, j]
                        
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







