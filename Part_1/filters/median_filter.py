from utils import *

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)

        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def filtreMed(img, vois):
    h, w = len(img), len(img[0])
    
    imgMed = np.zeros((h, w))

    for y in my_range(h):
        for x in my_range(w):
            m = int((vois - 1) / 2)
            if y < m or y >= h - m or x < m or x >= w - m:
                imgMed[y, x] = img[y, x]
            else:
                imgv = [img[yv][xv] for yv in my_range(y + m + 1, start=y - m) for xv in my_range(x + m + 1, start=x - m)]

                
                quicksort(imgv, 0, len(imgv) - 1)

                #median index
                imgMed[y, x] = imgv[int((vois * vois - 1) / 2)]

                # Clamp to valid range [0, 255]
                imgMed[y, x] = max(0, min(255, imgMed[y, x]))

    return np.array(imgMed, dtype=np.uint8)
