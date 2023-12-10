import numpy as np
import cv2
import sys
import warnings
warnings.filterwarnings('ignore')

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_directory)
from Part_1.filters.morphologic_filter import closing

class invisibility_cloak:
    """
    Function to transform a BGR pixel to an HSV one with the formulas :
    V = max( B, G, R )
    S = V if V!=0
      = 0 else
    H = 60* ( G-B ) / ( V - min(B, G, R) ) if V == R
      = 60* ( 2 + ( B-R ) / ( V - min(B, G, R) ) ) if V == G
      = 60* ( 4 + ( R-G ) / ( V - min(B, G, R) ) ) if V == B
    """
    def BGR2HSV_color(self, color):
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

    # Function to transform a BGR image to an HSV one
    def BGR2HSV(self, img):
        height, width, channels = img.shape
        hsv_image = np.zeros_like(img)

        for i in range(height):
            for j in range(width):
                hsv_image[i, j] = self.BGR2HSV_color(img[i, j])

        return hsv_image

    # Function to get a mask of a matrix where pixels are in range [lower_bound, upper_bound]
    def custom_inRange(self, image, lower_bound, upper_bound):
        result = np.zeros_like(image[:, :, 0])

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                pixel = image[i, j]

                if (
                    lower_bound[0] <= pixel[0] <= upper_bound[0]
                    and lower_bound[1] <= pixel[1] <= upper_bound[1]
                    and lower_bound[2] <= pixel[2] <= upper_bound[2]
                ):
                    result[i, j] = 255

        return result

    # Function to detect an object by a giving color
    # hue_range : tuple. 1st element is the lower hue value for a color, 2nd element is the higher hue value for a color (from a color map)
    def object_color_detection(self, img, hue_range):
        # trnasform to HSV, to more accurate results
        hsv_img = self.BGR2HSV( img )

        # create lower_bound and upper_bound of the color in the color map
        # we put saturation=50 so we can detect the color in all saturation values, with avoiding too much ligth colors which leed to white color
        # we put value=50 so we can detect the color in all luminance values, with avoiding too much dark colors which leed to black color
        lower_bound = np.array([hue_range[0], 50, 50])
        upper_bound = np.array([hue_range[1], 255, 255])

        return self.custom_inRange(hsv_img, lower_bound, upper_bound)

    # perform and operation between an array and a mask, we return an array with pixels only in the same position as the mask One pixels
    def and_operation(self, arr, mask):
        height, width = mask.shape
        result = np.zeros_like(arr)

        for i in range(height):
            for j in range(width):
                if mask[i, j] == 255:
                    result[i, j] = arr[i, j]

        return result

    # invert zeros and ones in an array
    def inverse_array_values(self, array):
        height, width = array.shape
        result = np.zeros_like(array)

        for i in range(height):
            for j in range(width):
                if array[i, j] == 0:
                    result[i, j] = 255

        return result

    # sum 2 arrays, we will need it in combining the background and image 
    def sum_arrays(self, arr1, arr2):
        height, width, _ = arr1.shape
        result = np.zeros_like(arr1)

        for i in range(height):
            for j in range(width):
                result[i, j] = arr1[i, j] + arr2[i, j]

        return result

    def run(self):
        # open the camera 
        capture_video = cv2.VideoCapture(0)

        # some seconds to capture the background accurately
        for i in range(20):
            return_val, background = capture_video.read()

        # flip background, so it can look more realistic
        # resize abackground to smallest size, so the processing doesn't take too much time
        if return_val:
            background = np.flip(background, axis=1)
            height, width, _ = background.shape
            background = cv2.resize( background, (256,256) )

        # while camera is opened 
        while capture_video.isOpened():
            # store frame at variable 'img'
            return_val, img = capture_video.read()
            if not return_val:
                break
            # flip image and resize it so we optimize time
            img = np.flip(img, axis=1)
            img = cv2.resize( img, (256,256) )

            # our cloak will be blue, we can change the color by changing the hue_range, for example hue values between 50 and 70 are green
            hue_range = (70, 100)  # blue

            # get a binary mask, where 1 means that the color of the correspondant pixel in the frame is detected as the desired color
            colored_object_mask = self.object_color_detection(img, hue_range)

            # perform closing filter, so we can close the holes in the frame if there are ones
            colored_object_mask = closing(colored_object_mask, 9, "rect", 1)

            # get the part of the background to be showed instead of the colored object in the frame
            background_to_show = self.and_operation(background, colored_object_mask)

            # get the part of the image to keep
            colored_object_mask_inverse = self.inverse_array_values(colored_object_mask)
            image_to_show = self.and_operation(img, colored_object_mask_inverse)

            # combine the 2 images 
            final_output = self.sum_arrays(background_to_show, image_to_show)

            # resize the frame to the original size of the camera 
            final_output = cv2.resize( final_output, (width, height) )

            cv2.imshow("Invisibility Cloak", final_output)
            # quit with 'Q' key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        capture_video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    invisibility_cloak().run()
