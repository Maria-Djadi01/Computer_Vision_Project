import sys
import cv2
import numpy as np

sys.path.append("../../Computer_Vision_Project")

from utils import *


def my_shape(img, gray=True):
    if gray:
        return (len(img), len(img[0]))
    else:
        return (len(img), len(img[0]), len(img[0][0]))


def my_copy(img, gray=True):
    # Get the dimensions of the image
    height = len(img)
    width = len(img[0])

    if gray:
        copy = [[0] * width for _ in my_range(height)]

        for i in my_range(height):
            for j in my_range(width):
                copy[i][j] = img[i][j]
    else:
        channels = len(img[0][0])

        copy = [[[0] * channels for _ in my_range(width)] for _ in my_range(height)]

        for i in my_range(height):
            for j in my_range(width):
                for k in my_range(channels):
                    copy[i][j][k] = img[i][j][k]

    return np.array(copy)


def my_range(stop, start=0, step=1):
    result = []

    current_value = start

    while current_value < stop:
        result.append(current_value)
        current_value += step

    return result


def my_max(a, b):
    return np.maximum(a, b)


def my_min(a, b):
    return np.minimum(a, b)


def generate_random_kernel(size, value_range=(1, 10)):
    kernel = np.random.randint(value_range[0], value_range[1] + 1, size=(size, size))
    print(kernel)
    sum = 0
    for i in my_range(size):
        for j in my_range(size):
            sum += kernel[i, j]
    return kernel / sum


def gaussian_filter(img):
    height, width = my_shape(img, gray=True)

    # kernel = np.array([[1, 2, 1],
    #                    [2, 4, 4],
    #                    [1, 2, 1]])
    # kernel = kernel / 16
    kernel = generate_random_kernel(3, value_range=(1, 10))

    img2 = my_copy(img)

    for y in my_range(height - 1, start=1):
        for x in my_range(width - 1, start=1):
            new_value = (
                kernel[0][0] * img[y - 1, x - 1]
                + kernel[0][1] * img[y - 1, x]
                + kernel[0][2] * img[y - 1, x + 1]
                + kernel[1][0] * img[y, x - 1]
                + kernel[1][1] * img[y, x]
                + kernel[1][2] * img[y, x + 1]
                + kernel[2][0] * img[y + 1, x - 1]
                + kernel[2][1] * img[y + 1, x]
                + kernel[2][2] * img[y + 1, x + 1]
            )

            img2[y, x] = my_max(0, my_min(255, new_value))

    return np.array(img2)


image = cv2.imread(r"Part_1\img.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Original Image", image)
cv2.imshow("Gaussian Filtered Image", gaussian_filter(image))
cv2.waitKey(0)
cv2.destroyAllWindows()
