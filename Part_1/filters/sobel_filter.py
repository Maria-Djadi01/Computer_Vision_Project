from utils import *


def sobel_filter(image):
    # Obtenir les dimensions de l'image
    height, width = len(image), len(image[0])

    # Define the Sobel kernels for horizontal and vertical edges
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # convolution pour les contours horizontaux
    edges_x = [[0] * width for _ in my_range(height)]
    for i in my_range(height - 1, start=1):
        for j in my_range(width - 1, start=1):
            pixel_value = (
                sobel_x[0][0] * image[i - 1][j - 1] +
                sobel_x[0][1] * image[i - 1][j] +
                sobel_x[0][2] * image[i - 1][j + 1] +
                sobel_x[1][0] * image[i][j - 1] +
                sobel_x[1][1] * image[i][j] +
                sobel_x[1][2] * image[i][j + 1] +
                sobel_x[2][0] * image[i + 1][j - 1] +
                sobel_x[2][1] * image[i + 1][j] +
                sobel_x[2][2] * image[i + 1][j + 1]
            )
            edges_x[i][j] = pixel_value

   # convolution pour les contours vericaux
    edges_y = [[0] * width for _ in my_range(height)]
    for i in my_range(height - 1, start=1):
        for j in my_range(width - 1, start=1):
            pixel_value = (
                sobel_y[0][0] * image[i - 1][j - 1] +
                sobel_y[0][1] * image[i - 1][j] +
                sobel_y[0][2] * image[i - 1][j + 1] +
                sobel_y[1][0] * image[i][j - 1] +
                sobel_y[1][1] * image[i][j] +
                sobel_y[1][2] * image[i][j + 1] +
                sobel_y[2][0] * image[i + 1][j - 1] +
                sobel_y[2][1] * image[i + 1][j] +
                sobel_y[2][2] * image[i + 1][j + 1]
            )
            edges_y[i][j] = pixel_value

    # Calcul du gradient
    gradient_magnitude = [[((edges_x[i][j])**2 + (edges_y[i][j])**2)**0.5 for j in my_range(width - 1, start=1)] for i in my_range(height - 1, start=1)]

    return np.array(gradient_magnitude, dtype=np.uint8)

