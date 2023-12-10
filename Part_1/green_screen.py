import cv2
import sys
from PIL import Image
sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")

from utils import get_limits, BGR2HSV, my_inRange, green_screen, BGR2HSV_color, my_copy, my_shape

class GreenScreen():
    def __init__(self, background):
        self.background = background
        self.color = None
        
        self.mask = None
        self.result = None
        self.cap_width = 320
        self.cap_height = 180
    
    def green_screen(self, mask, img, back):
        result = my_copy(img, gray=False)
        height, width, channels = my_shape(img, gray=False)

        for i in range(height):
            for j in range(width):
                if mask[i, j] == 255:
                    result[i, j] = back[i, j]
        return result
    
    def run(self):
        # Open the camera
        cap = cv2.VideoCapture(0)


        # Set the width and height properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)
        i = 1

        # Load the background image
        back = cv2.imread(self.background)
        back = cv2.resize(back, (self.cap_width, self.cap_height))
        # cv2.imshow('back', back)

        i = 1
        while True:
            ret, frame = cap.read()
            if i <= 100:
                # Display a message to place an object in a circle for color detection
                # Update color variable after a certain number of frames
                # Show the video frame with instructions
                frame = cv2.flip(frame, 1)
                x = int(self.cap_width / 4)
                y = int(self.cap_height / 2)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), 2)
                # write a message to tell to replace the object in the circle
                cv2.putText(
                    frame,
                    # write a flipped message
                    f"Place the object in the circle",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                ) 
                cv2.putText(
                    frame,
                    # write a flipped message
                    f"The color will be detect in {25 - i // 4}",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                ) 
                b, g, r = tuple(frame[y, x])
                cv2.imshow("frame", frame)
                i += 1
                color = b, g, r
            else:
                hsv_color = BGR2HSV_color(color)
                hsv_img = BGR2HSV(frame)
                lower_b, upper_b = get_limits(hsv_color, 20, 100, 100)
                mask = my_inRange(hsv_img, lower_b, upper_b)
                result = self.green_screen(mask, frame, back)
                cv2.imshow('frame', cv2.flip(frame, 1))
                cv2.imshow('mask', cv2.flip(mask, 1))
                cv2.imshow('result', cv2.flip(result, 1))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



        cap.release()
        cv2.destroyAllWindows()

# # Open the camera
# cap = cv2.VideoCapture(0)

# # Specify the desired width and height
# desired_width = 180
# desired_height = 320


# # Set the width and height properties
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
# i = 1

# # Load the background image
# back = cv2.imread("D:\\2M\Vision\Computer_Vision_Project\\back.jpg")
# back = cv2.resize(back, (352, 288))
# # cv2.imshow('back', back)

# i = 1
# while True:
#     ret, frame = cap.read()
#     if i <= 100:
#         x = int(desired_width / 4)
#         y = int(desired_height / 2)
#         cv2.circle(frame, (x, y), 5, (0, 255, 0), 2)
#         b, g, r = tuple(frame[y, x])
#         cv2.imshow('frame', cv2.flip(frame, 1))
#         i += 1
#         color = b, g, r
#         # print(color)
#     else:
#         hsv_color = BGR2HSV_color(color)
#         hsv_img = BGR2HSV(frame)
#         lower_b, upper_b = get_limits(hsv_color)
#         mask = my_inRange(hsv_img, lower_b, upper_b)
#         result = green_screen(mask, frame, back)
#         cv2.imshow('frame', cv2.flip(frame, 1))
#         cv2.imshow('mask', cv2.flip(mask, 1))
#         cv2.imshow('result', cv2.flip(result, 1))
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break



# cap.release()
# cv2.destroyAllWindows()

if __name__ == "__main__":
    green_screen = GreenScreen("D:/2M/Vision/Computer_Vision_Project/back.jpg")
    green_screen.run()