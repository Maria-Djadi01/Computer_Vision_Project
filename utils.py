import cv2
import numpy as np
import sys

sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")

from Part_1.filters.morphologic_filter import opening, closing


def my_max(a, b):
    return np.maximum(a, b)


def my_min(a, b):
    return np.minimum(a, b)


def my_max1(l):
    return max(l)


def my_min1(l):
    return min(l)


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
    height = len(img)
    width = len(img[0])

    if gray:
        # Create a 2D array
        copy = [[0] * width for _ in my_range(height)]

        for i in my_range(height):
            for j in my_range(width):
                # Assign the grayscale value directly
                copy[i][j] = img[i][j]
    else:
        channels = len(img[0][0])

        copy = [[[0] * channels for _ in my_range(width)] for _ in my_range(height)]

        for i in my_range(height):
            for j in my_range(width):
                for k in my_range(channels):
                    # Assign the color values to the corresponding channels
                    copy[i][j][k] = img[i][j][k]

    return np.array(copy)


def BGR2HSV_color(color):
    b, g, r = color[0], color[1], color[2]

    # Calculate Value (brightness)
    v = max(b, g, r)

    # Calculate Saturation
    if v == 0:
        s = 0
    else:
        s = int(((v - min(b, g, r)) / v) * 255)

    # Calculate Hue
    if v == min(b, g, r):
        h = 0  # undefined, set to 0
    elif v == r:
        h = int(60 * (g - b) / (v - min(b, g, r)))
    elif v == g:
        h = int(60 * (2 + (b - r) / (v - min(b, g, r))))
    elif v == b:
        h = int(60 * (4 + (r - g) / (v - min(b, g, r))))

    # Normalize to the range [0, 255]
    h = (h + 360) % 360  # Ensure hue is positive
    h = int((h / 360) * 255)
    v = int((v / 255) * 255)

    return h, s, v


def BGR2HSV(img):
    height, width, channels = my_shape(img, gray=False)
    hsv_image = my_copy(img, gray=False)

    for i in my_range(height):
        for j in my_range(width):
            hsv_image[i, j] = BGR2HSV_color(img[i, j])

    return hsv_image


def get_limits(hsv_color, h_limit, s_limit, v_limit):
    upper_bound = hsv_color[0] + h_limit, hsv_color[1] + s_limit, hsv_color[2] + v_limit
    lower_bound = hsv_color[0] - h_limit, hsv_color[1] - s_limit, hsv_color[2] - v_limit

    return lower_bound, upper_bound


def my_inRange(img, lower_bound, upper_bound):
    height, width, _ = my_shape(img, gray=False)
    mask = np.zeros((height, width), np.uint8)

    for i in range(height):
        for j in range(width):
            if (
                img[i, j][0] >= lower_bound[0]
                and img[i, j][0] <= upper_bound[0]
                and img[i, j][1] >= lower_bound[1]
                and img[i, j][1] <= upper_bound[1]
                and img[i, j][2] >= lower_bound[2]
                and img[i, j][2] <= upper_bound[2]
            ):
                mask[i, j] = 255
            else:
                mask[i, j] = 0
    return mask


# ---------------------------------------------------------------
# Enhancement functions
# ---------------------------------------------------------------
def remove_noise(mask, kernel_size=3):
    dilation_kernel = np.ones((kernel_size, kernel_size), np.uint8)

    mask_en = opening(mask, 3, "cross")

    return mask_en


def calculate_centroid(mask):
    # Calculate image moments
    moments = {"m00": 0, "m10": 0, "m01": 0}

    height, width = my_shape(mask)
    for i in range(height):
        row = mask[i]
        for j in range(width):
            if row[j] == 255:
                moments["m00"] += 1
                moments["m10"] += j
                moments["m01"] += i

    centroid_x = int(moments["m10"] / moments["m00"]) if moments["m00"] != 0 else 0
    centroid_y = int(moments["m01"] / moments["m00"]) if moments["m00"] != 0 else 0

    return (centroid_x, centroid_y)


def get_points(mask):
    points = []
    for i in range(len(mask)):
        for j in range(len(mask[0])):
            if mask[i][j] == 255:
                points.append((j, i))
    return points


# ----------------------------------------------------------------
# Object detection function
# ----------------------------------------------------------------


def detect_color_object(img, color, h_limit, s_limit, v_limit):
    hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)[0][0]
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_b, upper_b = get_limits(hsv_color, h_limit, s_limit, v_limit)
    mask = my_inRange(hsv_img, lower_b, upper_b)
    mask = remove_noise(mask)
    # calculate the centroid of the object
    centroid_x, centroid_y = calculate_centroid(mask)
    return img, mask, [[centroid_x, centroid_y]]


# ----------------------------------------------------------------
# Green screen function
# ----------------------------------------------------------------
def green_screen(mask, img, back):
    result = my_copy(img, gray=False)
    height, width, channels = my_shape(img, gray=False)

    for i in my_range(height):
        for j in my_range(width):
            if mask[i, j] == 255:
                result[i, j] = back[i, j]
    return result


# # try mask fun
# img = cv2.imread("D:\\2M\Vision\Computer_Vision_Project\\bleu.png")
# color = (0, 0, 255)
# mask = detect_color_object(img, color)
# cv2.imshow("mask", mask)
# cv2.imshow("img", img)
# # cv2.imshow("img hsv", hsv_img)
# # cv2.imshow("cv hsv", hsv_img_cv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
