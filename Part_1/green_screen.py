import cv2
import sys
from PIL import Image
sys.path.insert(0, "C:\Users\HI\My-Github\Computer_Vision_Project")

from utils import get_limits, BGR2HSV, my_inRange, green_screen, BGR2HSV_color

# Open the camera
cap = cv2.VideoCapture(0)

# Specify the desired width and height
desired_width = 180
desired_height = 320


# Set the width and height properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
i = 1

# Load the background image
back = cv2.imread("D:\\2M\Vision\Computer_Vision_Project\\back.jpg")
back = cv2.resize(back, (352, 288))
# cv2.imshow('back', back)

i = 1
while True:
    ret, frame = cap.read()
    if i <= 100:
        x = int(desired_width / 4)
        y = int(desired_height / 2)
        cv2.circle(frame, (x, y), 5, (0, 255, 0), 2)
        b, g, r = tuple(frame[y, x])
        cv2.imshow('frame', cv2.flip(frame, 1))
        i += 1
        color = b, g, r
        # print(color)
    else:
        hsv_color = BGR2HSV_color(color)
        hsv_img = BGR2HSV(frame)
        lower_b, upper_b = get_limits(hsv_color)
        mask = my_inRange(hsv_img, lower_b, upper_b)
        result = green_screen(mask, frame, back)
        cv2.imshow('frame', cv2.flip(frame, 1))
        cv2.imshow('mask', cv2.flip(mask, 1))
        cv2.imshow('result', cv2.flip(result, 1))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()