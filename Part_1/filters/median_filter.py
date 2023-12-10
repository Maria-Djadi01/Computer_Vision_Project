from utils import *


def partition(arr, low, high):
    # Choix du pivot comme élément le plus à droite
    pivot = arr[high]
    i = low - 1
    # placement des éléments plus petits que le pivot à gauche, et plus grands à droite
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    # Placement du pivot à la bonne position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(arr, low, high):
    # Tri rapide récursif
    if low < high:
        pi = partition(arr, low, high)

        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)


def median_filter(img, vois):
    # Obtenir les dimensions de l'image
    h, w = len(img), len(img[0])
    # Initialisation de l'image filtrée
    imgMed = np.zeros((h, w))
    #parcourir les pixels
    for y in my_range(h):
        for x in my_range(w):
            # Calculer la distance separant le pixel central et les bords du voisinage(pour savoir si le voisinage depasse)
            m = int((vois - 1) / 2)
            # Vérifier si le pixel est près de la bordure de l'image
            if y < m or y >= h - m or x < m or x >= w - m:
                # si oui, garder le pixel tel quel
                imgMed[y, x] = img[y, x]
            else:
                #sinon , xtraction des valeurs du voisinage dans une liste
                imgv = [ img[yv][xv]
                    for yv in my_range(y + m + 1, start=y - m)
                    for xv in my_range(x + m + 1, start=x - m)
                ]
                # Trier la liste
                quicksort(imgv, 0, len(imgv) - 1)
                # Calcul de la valeur médiane à partir de la liste triée
                imgMed[y, x] = imgv[int((vois * vois - 1) / 2)]
                 # Limiter la valeur médiane à la plage valide [0, 255]
                imgMed[y, x] = max(0, min(255, imgMed[y, x]))

    return np.array(imgMed, dtype=np.uint8)
