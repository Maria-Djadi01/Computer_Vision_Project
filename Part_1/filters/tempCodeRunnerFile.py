
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