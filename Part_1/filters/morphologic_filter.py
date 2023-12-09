import math
import cv2
import numpy as np

"""
parameters : 
    kernel_size : odd numbers only.
    kernel_shape : 'rect', 'cross', 'ellipse'.
    iterations : optional, by default 1.
"""

# ------------------ Dilation
def dilation( img, kernel_size, kernel_shape, iterations=1 ) :
    if kernel_shape == 'rect' :
        kernel_list = [ [1 for i in range(kernel_size)] for j in range(kernel_size) ]
        kernel = np.array( kernel_list )
    elif kernel_shape == 'cross' :
        kernel_list = [
            [1 if i == kernel_size // 2 or j == kernel_size // 2 else 0 for i in range(kernel_size)]
            for j in range(kernel_size)
        ]
        kernel = np.array( kernel_list )
    elif kernel_shape == 'ellipse' :
        kernel = np.zeros((kernel_size, kernel_size), dtype=np.uint8)
        center = (kernel_size - 1) / 2
        radius = center
        for i in range(kernel_size):
            for j in range(kernel_size):
                if ((i - center) / radius) ** 2 + ((j - center) / radius) ** 2 <= 1:
                    kernel[i, j] = 1
                    
    height, width = img.shape
    img_result = np.zeros( (height, width) )

    for iteration in range(iterations) :
        i = 0
        while i < height :
            
            j = 0
            while j < width :
                
                if img[i, j] == 255 :
                    
                    h = 0
                    while h < kernel_size :
                        
                        w = 0
                        while w < kernel_size :
                            
                            if kernel[h, w] == 1 :
                                row = i - kernel_size // 2 + h
                                col = j - kernel_size // 2 + w
                                if(height>row>=0 and width>col>=0 ) :
                                    img_result[row, col] = 255
                                
                            w += 1
                    
                        h += 1
                        
                j += 1
                
            i += 1
         
        img = img_result.copy()
        
    return img_result

# ------------------ Erosion
def erosion( img, kernel_size, kernel_shape, iterations=1 ) :
    if kernel_shape == 'rect' :
        kernel_list = [ [1 for i in range(kernel_size)] for j in range(kernel_size) ]
        kernel = np.array( kernel_list )
    elif kernel_shape == 'cross' :
        kernel_list = [
            [1 if i == kernel_size // 2 or j == kernel_size // 2 else 0 for i in range(kernel_size)]
            for j in range(kernel_size)
        ]
        kernel = np.array( kernel_list )
    elif kernel_shape == 'ellipse' :
        kernel = np.zeros((kernel_size, kernel_size), dtype=np.uint8)
        center = (kernel_size - 1) / 2
        radius = center
        for i in range(kernel_size):
            for j in range(kernel_size):
                if ((i - center) / radius) ** 2 + ((j - center) / radius) ** 2 <= 1:
                    kernel[i, j] = 1
                    
    height, width = img.shape
    img_result = np.zeros( (height, width) )

    for iteration in range(iterations) :
        i = 0
        while i < height :
            
            j = 0
            while j < width :
                
                if img[i, j] == 255 :
                    
                    all_pixels_are_one = True
                    h = 0
                    while h < kernel_size :
                        
                        w = 0
                        while w < kernel_size :
                            if kernel[h, w] == 1 :
                                row = i - kernel_size // 2 + h
                                col = j - kernel_size // 2 + w
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

        img = img_result.copy()

    return img_result

# ------------------ Opening
def opening( img, kernel_size, kernel_shape, iterations=1 ) :
    return dilation( erosion( img, kernel_size, kernel_shape, iterations=1 ), kernel_size, kernel_shape, iterations=1 )

# ------------------ Closing
def closing( img, kernel_size, kernel_shape, iterations=1 ) :
    return erosion( dilation( img, kernel_size, kernel_shape, iterations=1 ), kernel_size, kernel_shape, iterations=1 )


# ------------------ Test examples
"""
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

img_result_dilation = dilation( img, 9, 'cross', iterations=2 )
img_result_erosion = erosion( img, 9, 'cross', iterations=2 )
img_result_opening = opening( img1, 9, 'cross', iterations=2 )
img_result_closing = closing( img2, 9, 'cross', iterations=2 )

cv2.imshow( "image originale", img )
cv2.imshow( "image originale 1", img1 )
cv2.imshow( "image originale 2", img2 )
cv2.imshow( "image dilation", img_result_dilation )
cv2.imshow( "image erosion", img_result_erosion )
cv2.imshow( "image opening", img_result_opening )
cv2.imshow( "image closing", img_result_closing )
cv2.waitKey(0)
cv2.destroyAllWindows()"""
