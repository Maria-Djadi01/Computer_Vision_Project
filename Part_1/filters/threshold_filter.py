import numpy as np
import cv2

""" 
parameters :
    thresh_type : 'binary' | 'binary_inv' | 'trunc' | 'tozero' | 'tozero_inv'
    threshold : in range (0, 255)
"""


def custom_threshold(img, threshold, thresh_type):
    height, width = img.shape

    if thresh_type == "binary":
        result_img = np.zeros_like(img)
        result_img[img > threshold] = 255
        return result_img

    elif thresh_type == "binary_inv":
        result_img = np.zeros_like(img)
        result_img[img <= threshold] = 255
        return result_img

    elif thresh_type == "trunc":
        result_img = img.copy()
        result_img[img > threshold] = threshold
        return result_img

    elif thresh_type == "tozero":
        result_img = img.copy()
        result_img[img <= threshold] = 0
        return result_img

    elif thresh_type == "tozero_inv":
        result_img = img.copy()
        result_img[img > threshold] = 0
        return result_img


# image = cv2.imread(r"Part_1\img.jpg", cv2.IMREAD_GRAYSCALE)
# cv2.imshow("Original Image", image)
# cv2.imshow("Threshold Filtered Image", custom_threshold(image, 2, "binary"))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
