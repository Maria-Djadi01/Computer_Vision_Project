from utils import *


def mean_filter(img, neighborhood):
    h, w = len(img), len(img[0])

    imgMoy = np.zeros((h, w))

    for y in my_range(h):
        for x in my_range(w):
            m = (neighborhood - 1) // 2
            if y < m or y >= h - m or x < m or x >= w - m:
                imgMoy[y, x] = img[y, x]
            else:
                imgv_sum = 0
                for yv in my_range(y + m + 1, start=y - m):
                    for xv in my_range(x + m + 1, start=x - m):
                        imgv_sum += img[yv, xv]
                moy = imgv_sum // (neighborhood * neighborhood)

                # Clamp to the valid range [0, 255]
                imgMoy[y, x] = max(0, min(255, moy))

    return np.array(imgMoy, dtype=np.uint8)


# img = cv2.imread("assets/link.jpg", cv2.IMREAD_GRAYSCALE)
# img = cv2.resize(img, (400, 400))
# cv2.imshow("Original Image", img)

# cv2.imshow("Filtered Image1", meanFilter(img, 3))
# # cv2.imshow("Filtered Image2", gaussian_filter(img))


# # cv2.imshow(" Filtered Image", sobel_filter(img))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
