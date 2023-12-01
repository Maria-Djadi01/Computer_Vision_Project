import cv2
import sys
from PIL import Image
sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")

from utils import detect_color_object

# Open the camera
cap = cv2.VideoCapture(0)

# Specify the desired width and height
desired_width = 160
desired_height = 120


# Set the width and height properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
i = 1
while True:
    ret, frame = cap.read()
    if i <= 50:
        x = int(desired_width / 4)
        y = int(desired_height / 2)
        cv2.circle(frame, (x, y), 5, (0, 255, 0), 2)
        b, g, r = tuple(frame[y, x])
        cv2.imshow('frame', cv2.flip(frame, 1))
        i += 1
        color = b, g, r
    else:
        mask = detect_color_object(frame, color, 10, 100, 100)
        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()
        if bbox:
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.imshow('frame', cv2.flip(frame, 1))
        cv2.imshow('mask', cv2.flip(mask, 1))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()