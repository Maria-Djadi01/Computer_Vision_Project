import numpy as np
import cv2

""" 
parameters :
    thresh_type : 'binary' | 'binary_inv' | 'trunc' | 'tozero' | 'tozero_inv'
    threshold : in range (0, 255)
"""

def custom_threshold(img, threshold, thresh_type):
    height, width = img.shape

    # Binary threshold : all pixels are 0. Except ones > threshold, they will have maxValue : 255
    if thresh_type == "binary":
        result_img = np.zeros_like(img)
        result_img[img > threshold] = 255
        return result_img

    # Binary_inv threshold : all pixels are 0. Except ones <= threshold, they will have maxValue : 255
    elif thresh_type == "binary_inv":
        result_img = np.zeros_like(img)
        result_img[img <= threshold] = 255
        return result_img

    # Truncated threshold : all pixels are the same as original image. 
    # Except ones > threshold, they will have threshold value
    elif thresh_type == "trunc":
        result_img = img.copy()
        result_img[img > threshold] = threshold
        return result_img

    # Tozero threshold : all pixels are the same as original image. 
    # Except ones <= threshold, they will have 0 value
    elif thresh_type == "tozero":
        result_img = img.copy()
        result_img[img <= threshold] = 0
        return result_img

    # Tozero_inv threshold : all pixels are the same as original image. 
    # Except ones > threshold, they will have 0 value
    elif thresh_type == "tozero_inv":
        result_img = img.copy()
        result_img[img > threshold] = 0
        return result_img
