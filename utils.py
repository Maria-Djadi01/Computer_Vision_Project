import cv2
import numpy as np


def my_max(a, b):
    return np.maximum(a, b)


def my_min(a, b):
    return np.minimum(a, b)


def my_range(stop, start=0, step=1):
    result = []

    current_value = start

    while current_value < stop:
        result.append(current_value)
        current_value += step

    return result


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
