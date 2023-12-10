import sys
import cv2
import numpy as np


def my_copy(img, gray=True):
    """
    Create a copy of the input image.

    Parameters:
    - img (numpy.ndarray): The input image.
    - gray (bool): Flag indicating whether the image is grayscale. Default is True.

    Returns:
    - numpy.ndarray: A copy of the input image.
    """
    # Get the dimensions of the image
    height, width = img.shape[:2]

    if gray:
        # Create a 2D array for grayscale image (filled with zeros)
        copy = [[0] * width for _ in range(height)]

        # Copy pixel values
        for i in range(height):
            for j in range(width):
                copy[i][j] = img[i][j]
    else:
        # Determine the number of color channels
        channels = len(img[0][0])

        # Create a 3D array for color image
        copy = [[[0] * channels for _ in range(width)] for _ in range(height)]

        # Copy pixel values for each channel
        for i in range(height):
            for j in range(width):
                for k in range(channels):
                    copy[i][j][k] = img[i][j][k]

    return np.array(copy)


def gaussian_filter(img):
    """
    Apply a Gaussian filter to the input grayscale image.

    Parameters:
    - img (numpy.ndarray): The input grayscale image.

    Returns:
    - numpy.ndarray: The image after applying the Gaussian filter.
    """
    # Get the dimensions of the image
    height, width = img.shape

    # Define the Gaussian kernel
    kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    kernel = kernel / 16

    # Create a copy of the input image
    img2 = my_copy(img)

    # Apply the Gaussian filter to the image
    for y in range(1, height - 1):
        for x in range(1, width - 1):
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

            # Clip the pixel value to the valid range [0, 255]
            img2[y, x] = max(0, min(255, new_value))

    return np.array(img2)


# image = cv2.imread(r"Part_1\img.jpg", cv2.IMREAD_GRAYSCALE)
# cv2.imshow("Original Image", image)
# cv2.imshow("Gaussian Filtered Image", gaussian_filter(image))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
