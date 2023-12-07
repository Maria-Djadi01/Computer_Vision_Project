import math
import cv2
import numpy as np

# ------------------ Dilation
def dilation( img, kernel ) :
    height, width = img.shape
    k_height, k_width = kernel.shape
    img_result = np.zeros( (height, width) )

    i = 0
    while i < height :
        
        j = 0
        while j < width :
            
            if img[i, j] == 255 :
                
                h = 0
                while h < k_height :
                    
                    w = 0
                    while w < k_width :
                        
                        if kernel[h, w] == 1 :
                            row = i - k_height // 2 + h
                            col = j - k_width // 2 + w
                            if(height>row>=0 and width>col>=0 ) :
                                img_result[row, col] = 255
                            
                        w += 1
                
                    h += 1
                    
            j += 1
            
        i += 1

    return img_result

# ------------------ Erosion
def erosion( img, kernel ) :
    height, width = img.shape
    k_height, k_width = kernel.shape
    img_result = np.zeros( (height, width) )

    i = 0
    while i < height :
        
        j = 0
        while j < width :
            
            if img[i, j] == 255 :
                
                all_pixels_are_one = True
                h = 0
                while h < k_height :
                    
                    w = 0
                    while w < k_width :
                        if kernel[h, w] == 1 :
                            row = i - k_height // 2 + h
                            col = j - k_width // 2 + w
                            if(height>row>=0 and width>col>=0) :
                                if img[row, col] != 255 :
                                    all_pixels_are_one = False
                                    break
                        
                        w += 1
                
                    if not all_pixels_are_one:
                        break
                    
                    h += 1
                    
                if all_pixels_are_one :
                    img_result[i, j] = 255
                    
            j += 1
            
        i += 1

    return img_result

# ------------------ Opening
def opening( img, kernel ) :
    return dilation( erosion( img, kernel ), kernel )
    
# ------------------ Closing
def closing( img, kernel ) :
    return erosion( dilation( img, kernel ), kernel )



# ------------------ Test

"""
img = [ [0,0,0,0,0,0,0], [255,0,0,0,0,0,0], [255,0,0,0,0,0,0], [255,255,0,0,0,0,0], [255,255,255,0,0,0,0], [255,255,255,0,0,0,0], [0,0,0,0,0,0,0] ]
img = np.array( img, dtype='uint8' )
dil = dilation( img, kernel )
eros = erosion( img, kernel )
print( img, '\n\n', dil, '\n\n', eros )"""

"""kernel = cv2.getStructuringElement( cv2.MORPH_CROSS, (9, 9) )
img_result_dilation = cv2.dilate( img, kernel )
img_result_erosion = cv2.erode( img, kernel )
img_result_opening = cv2.morphologyEx( img1, cv2.MORPH_OPEN, kernel )
img_result_closing = cv2.morphologyEx( img2, cv2.MORPH_CLOSE, kernel )"""

img = cv2.imread( "j.png", 0 )
img1 = cv2.imread( "j1.png", 0 )
img2 = cv2.imread( "j2.png", 0 )

cv2.threshold( img, 130, 255, 0, img )
cv2.threshold( img1, 130, 255, 0, img1 )
cv2.threshold( img2, 130, 255, 0, img2 )

kernel = np.array([[0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0]])

img_result_dilation = dilation( img, kernel )
img_result_erosion = erosion( img, kernel )
img_result_opening = opening( img1, kernel )
img_result_closing = closing( img2, kernel )

cv2.imshow( "image originale", img )
cv2.imshow( "image originale 1", img1 )
cv2.imshow( "image originale 2", img2 )
cv2.imshow( "image dilation", img_result_dilation )
cv2.imshow( "image erosion", img_result_erosion )
cv2.imshow( "image opening", img_result_opening )
cv2.imshow( "image closing", img_result_closing )
cv2.waitKey(0)
cv2.destroyAllWindows()














