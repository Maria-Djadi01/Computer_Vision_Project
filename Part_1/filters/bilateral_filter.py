from utils import *

def bilateral_filter(image, neighborhood_size, spatial_sigma, intensity_sigma):
    height, width = image.shape
    result = np.zeros((height, width))

    half_size = neighborhood_size // 2

    for y in range(height):
        for x in range(width):
            weight_sum = 0
            filtered_value = 0

            for i in my_range( half_size + 1, start = -half_size):
                for j in my_range(half_size + 1, start = -half_size):
                    neighbor_y, neighbor_x = y + i, x + j

                    if 0 <= neighbor_y < height and 0 <= neighbor_x < width:
                        spatial_diff = (i**2 + j**2)**0.5
                        intensity_diff = abs(float(image[y, x]) - float(image[neighbor_y, neighbor_x]))

                        spatial_weight = 2.71828**(-(spatial_diff**2) / (2 * spatial_sigma**2))
                        intensity_weight = 2.71828**(-(intensity_diff**2) / (2 * intensity_sigma**2))

                        weight = spatial_weight * intensity_weight
                        weight_sum += weight
                        filtered_value += weight * float(image[neighbor_y, neighbor_x])

            result[y, x] = filtered_value / weight_sum

    return np.array(result, dtype=np.uint8)
