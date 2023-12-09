import numpy as np
import cv2
import sys

sys.path.insert(0, r"C:\\Users\\HI\\My-Github\\Computer_Vision_Project")
from Part_1.filters.morphologic_filter import closing

class invisibility_cloak :
    
    def BGR2HSV_color(self,color):
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
    
    def BGR2HSV(self,img):
        height, width, channels = img.shape
        hsv_image = np.zeros_like( img )
    
        for i in range(height):
            for j in range(width):
                hsv_image[i, j] = self.BGR2HSV_color(img[i, j])
    
        return hsv_image
    
    def custom_inRange( self, image, lower_bound, upper_bound ):
        result = np.zeros_like( image[:,:,0] )
    
        for i in range( image.shape[0] ):
            for j in range( image.shape[1] ):
                pixel = image[i, j]
    
                if lower_bound[0] <= pixel[0] <= upper_bound[0] and \
                   lower_bound[1] <= pixel[1] <= upper_bound[1] and \
                   lower_bound[2] <= pixel[2] <= upper_bound[2] :
                    result[i, j] = 255
    
        return result
    
    def object_color_detection( self, img, hue_range ) :
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #hsv_img = BGR2HSV( img )
        
        lower_bound = np.array( [hue_range[0], 50, 50] )
        upper_bound = np.array( [hue_range[1], 255, 255] )
        
        return self.custom_inRange( hsv_img, lower_bound, upper_bound )
    
    
    
    def and_operation( self, arr, mask ) :
        height, width = mask.shape
        result = np.zeros_like( arr )
        
        for i in range( height ) :
            for j in range( width ) :
                if mask[i, j] == 255 :
                    result[i, j] = arr[i, j]
    
        return result
    
    def inverse_array_values( self, array ) :
        height, width = array.shape
        result = np.zeros_like( array )
        
        for i in range( height ) :
            for j in range( width ) :
                if array[i, j] == 0 :
                    result[i, j] = 255
                    
        return result
    
    def sum_arrays( self, arr1, arr2 ) :
        height, width, _ = arr1.shape
        result = np.zeros_like( arr1 )
        
        for i in range( height ) :
            for j in range( width ) :
                result[i, j] = arr1[i, j] + arr2[i, j]
                
        return result
    
    def run(self) :
        capture_video = cv2.VideoCapture(0) 
        for i in range(20) :
            return_val, background = capture_video.read() 
        if return_val :
            background = np.flip( background, axis = 1 )
            
        while (capture_video.isOpened()): 
            return_val, img = capture_video.read() 
            if not return_val : 
                break 
            img = np.flip( img, axis = 1 ) 
            
            hue_range = (70, 100) # blue
            colored_object_mask = self.object_color_detection( img, hue_range )
            colored_object_mask = closing( colored_object_mask, 9, 'cross' )
            background_to_show = self.and_operation( background, colored_object_mask ) 
            
            colored_object_mask_inverse = self.inverse_array_values( colored_object_mask )
            image_to_show = self.and_operation( img, colored_object_mask_inverse ) 
            
            final_output = self.sum_arrays( background_to_show, image_to_show )
            
            cv2.imshow( "Invisibility Cloak", final_output ) 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        capture_video.release()
        cv2.destroyAllWindows()
        
cloak = invisibility_cloak()
cloak.run()
