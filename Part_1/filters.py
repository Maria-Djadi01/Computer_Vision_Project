# The filters that should be implemented:
# Mean Filter, Median Filter, Gaussian Filter, Laplace Filter, 2D Filter
import sys

sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")

from utils import *
from Part_1.filters.laplacian_filter import laplacian_filter

image = cv2.imread(
    "D:\\2M\Vision\Computer_Vision_Project\Part_1\img.jpg", cv2.IMREAD_GRAYSCALE
)
cv2.imshow("Original Image", image)
cv2.imshow("Laplacian Filtered Image From Scratch", laplacian_filter(image))
cv2.waitKey(0)
cv2.destroyAllWindows()
