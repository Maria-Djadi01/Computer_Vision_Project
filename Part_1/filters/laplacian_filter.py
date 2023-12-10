import sys
import os

# Get the project's root directory
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project's root directory to sys.path
sys.path.insert(0, project_directory)

from utils import *

def laplacian_filter(image, kernel_size=3):
    """
    Apply the Laplacian filter to an image.

    Parameters:
    - image: Input image.
    - kernel_size: Size of the square Laplacian filter kernel (default is 3).

    Returns:
    - np.array: Filtered image.
    """

    # Get the dimensions of the image
    height, width = my_shape(image, gray=True)

    # Build the Laplacian kernel
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
    kernel *= -1
    kernel[kernel_size // 2][kernel_size // 2] = kernel_size * kernel_size - 1

    # Apply convolution to the image
    filtered_image = my_copy(image)

    # Iterate over the image pixels
    for i in my_range(height - 1, start=1):
        for j in my_range(width - 1, start=1):
            # Convolution operation with the Laplacian kernel
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

            # Clip the pixel values to the valid range [0, 255]
            filtered_image[i, j] = my_max(0, my_min(255, pixel_value))

    return np.array(filtered_image)
