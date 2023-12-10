import sys
import cv2
import numpy as np

def my_copy(img, gray=True):
    # Get the dimensions of the image
    height = len(img)
    width = len(img[0])

    if gray:
        copy = [[0] * width for _ in range(height)]

        for i in range(height):
            for j in range(width):
                copy[i][j] = img[i][j]
    else:
        channels = len(img[0][0])

        copy = [[[0] * channels for _ in range(width)] for _ in range(height)]

        for i in range(height):
            for j in range(width):
                for k in range(channels):
                    copy[i][j][k] = img[i][j][k]

    return np.array(copy)


def gaussian_filter(img):
    height, width = img.shape

    kernel = np.array([[1, 2, 1], [2, 4, 4], [1, 2, 1]])
    kernel = kernel / 16

    img2 = my_copy(img)

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

            img2[y, x] = max(0, min(255, new_value))

    return np.array(img2)


# image = cv2.imread(r"Part_1\img.jpg", cv2.IMREAD_GRAYSCALE)
# cv2.imshow("Original Image", image)
# cv2.imshow("Gaussian Filtered Image", gaussian_filter(image))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
