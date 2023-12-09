import numpy as np
import cv2

def BGR2HSV_color(color):
    b, g, r = color[0], color[1], color[2]

    # Calculate Value (brightness)
    v = max(b, g, r)

    # Calculate Saturation
    if v == 0:
        s = 0
    else:
        s = round(((v - min(b, g, r)) / v) * 255)

    # Calculate Hue
    if v == min(b, g, r):
        h = 0  # undefined, set to 0
    elif v == r:
        h = round(60 * (g - b) / (v - min(b, g, r)))
    elif v == g:
        h = round(60 * (2 + (b - r) / (v - min(b, g, r))))
    elif v == b:
        h = round(60 * (4 + (r - g) / (v - min(b, g, r))))

    # Normalize to the range [0, 180]
    h = (h + 360) % 360  # Ensure hue is positive
    h = round((h / 360) * 180)

    return h, s, v

def BGR2HSV(img):
    height, width, channels = img.shape
    hsv_image = np.zeros_like( img )

    for i in range(height):
        for j in range(width):
            hsv_image[i, j] = BGR2HSV_color(img[i, j])

    return hsv_image

def custom_inRange( image, lower_bound, upper_bound ):
    result = np.zeros_like( image[:,:,0] )

    for i in range( image.shape[0] ):
        for j in range( image.shape[1] ):
            pixel = image[i, j]

            if lower_bound[0] <= pixel[0] <= upper_bound[0] and \
               lower_bound[1] <= pixel[1] <= upper_bound[1] and \
               lower_bound[2] <= pixel[2] <= upper_bound[2] :
                result[i, j] = 255

    return result

def object_color_detection( img, hue_range ) :
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #hsv_img = BGR2HSV( img )
    
    lower_bound = np.array( [hue_range[0], 50, 50] )
    upper_bound = np.array( [hue_range[1], 255, 255] )
    
    return custom_inRange( hsv_img, lower_bound, upper_bound )

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
    
# ------------------ Closing
def closing( img, kernel ) :
    return erosion( dilation( img, kernel ), kernel )

def and_operation( arr, mask ) :
    height, width = mask.shape
    result = np.zeros_like( arr )
    
    for i in range( height ) :
        for j in range( width ) :
            if mask[i, j] == 255 :
                result[i, j] = arr[i, j]

    return result

def inverse_array_values( array ) :
    height, width = array.shape
    result = np.zeros_like( array )
    
    for i in range( height ) :
        for j in range( width ) :
            if array[i, j] == 0 :
                result[i, j] = 255
                
    return result

def sum_arrays( arr1, arr2 ) :
    height, width, _ = arr1.shape
    result = np.zeros_like( arr1 )
    
    for i in range( height ) :
        for j in range( width ) :
            result[i, j] = arr1[i, j] + arr2[i, j]
            
    return result

capture_video = cv2.VideoCapture(0) 
for i in range(30) :
    return_val, background = capture_video.read() 
if return_val :
    background = np.flip( background, axis = 1 )
    
while (capture_video.isOpened()): 
    return_val, img = capture_video.read() 
    if not return_val : 
        break 
    img = np.flip( img, axis = 1 ) 
  
    hue_range = (70, 100) # cyan color 
    colored_object_mask = object_color_detection( img, hue_range )
    kernel = np.array([[0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0]])
    colored_object_mask = closing( colored_object_mask, kernel )
    background_to_show = and_operation( background, colored_object_mask ) 
    
    colored_object_mask_inverse = inverse_array_values( colored_object_mask )
    image_to_show = and_operation( img, colored_object_mask_inverse ) 
    
    final_output = sum_arrays( background_to_show, image_to_show )
    
    cv2.imshow( "Invisibility Cloak", final_output ) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
capture_video.release()
cv2.destroyAllWindows()
