import numpy as np
import cv2

def custom_threshold( img, threshold, thresh_type ) :
    height, width = img.shape
    
    if thresh_type == 'binary' :
        result_img = np.zeros_like( img )
        result_img[img > threshold] = 255
        return result_img
    
    elif thresh_type == 'binary_inv' :
        result_img = np.zeros_like( img )
        result_img[img <= threshold] = 255
        return result_img
    
    elif thresh_type == 'trunc' :
        result_img = img.copy()
        result_img[img > threshold] = threshold
        return result_img
    
    elif thresh_type == 'tozero' :
        result_img = img.copy()
        result_img[img <= threshold] = 0
        return result_img
    
    elif thresh_type == 'tozero_inv' :
        result_img = img.copy()
        result_img[img > threshold] = 0
        return result_img
    

img = cv2.imread( "img.png", 0 )

custom = custom_threshold( img, 150, 'trunc' )
with_cv = cv2.threshold( img, 150, 255, cv2.THRESH_TRUNC )[1]

cv2.imshow( "image originale", img )
cv2.imshow( "image filtre", custom )
cv2.imshow( "image cv2", with_cv )

cv2.waitKey(0)
cv2.destroyAllWindows()





















