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