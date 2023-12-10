from utils import *


def mean_filter(img, neighborhood):
    # Obtenir les dimensions de l'image
    h, w = len(img), len(img[0])
    # Initialiser l'image filtrée
    imgMoy = np.zeros((h, w))
    #parcourir les pixels
    for y in my_range(h):
        for x in my_range(w):
            # Calculer la distance separant le pixel central et les bords du voisinage(pour savoir si le voisinage depasse)
            m = (neighborhood - 1) // 2
            # Vérifier si le pixel est près de la bordure de l'image
            if y < m or y >= h - m or x < m or x >= w - m:
                # si oui, garder le pixel tel quel
                imgMoy[y, x] = img[y, x]
            else:
                #sinon, calculer la moyenne des pixels de son voisinage
                imgv_sum = 0
                for yv in my_range(y + m + 1, start=y - m):
                    for xv in my_range(x + m + 1, start=x - m):
                        imgv_sum += img[yv, xv]
                moy = imgv_sum // (neighborhood * neighborhood)

                # limiter le resultat a la plage valide [0, 255]
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
