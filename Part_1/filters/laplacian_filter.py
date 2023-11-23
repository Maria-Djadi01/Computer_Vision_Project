import sys

sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")
from utils import *


def laplacian_filter(image):
    # Get the dimensions of the image
    height, width = my_shape(image, gray=True)

    # Define the Laplacian kernel
    kernel = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

    # Apply convolution to the image
    filtered_image = my_copy(image)

    for i in my_range(height - 1, start=1):
        for j in my_range(width - 1, start=1):
            pixel_value = (
                kernel[0][0] * image[i - 1, j - 1]
                + kernel[0][1] * image[i - 1, j]
                + kernel[0][2] * image[i - 1, j + 1]
                + kernel[1][0] * image[i, j - 1]
                + kernel[1][1] * image[i, j]
                + kernel[1][2] * image[i, j + 1]
                + kernel[2][0] * image[i + 1, j - 1]
                + kernel[2][1] * image[i + 1, j]
                + kernel[2][2] * image[i + 1, j + 1]
            )

            # Reduc the pixel values to the valid range [0, 255]
            filtered_image[i, j] = my_max(0, my_min(255, pixel_value))

    return np.array(filtered_image)
