import cv2
import sys
from PIL import Image

sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")

from utils import detect_color_object

class ObjectDetector(object):
    def __init__(self):
        """
        Initialize the ObjectDetector.

        Attributes:
        - color: Color of the object to be detected.
        - mask: Binary mask indicating the region where the color is detected.
        - result: Resulting image with object detection highlighted.
        - cap_width: Width of the camera frame.
        - cap_height: Height of the camera frame.
        """
        self.color = None
        self.mask = None
        self.result = None
        self.cap_width = 320
        self.cap_height = 180
    
    def run(self):
        # Open the camera
        cap = cv2.VideoCapture(0)

        # Set the width and height properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        i = 1
        while True:
            ret, frame = cap.read()
            if i <= 200:
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
                # Detect color object in the frame using a utility function
                frame, mask, points = detect_color_object(frame, color, 20, 100, 100)
                if len(points) > 0:
                    # Display a circle around the detected object
                    cv2.circle(frame, points[0], 10, (0, 255, 0), 2)
                cv2.imshow("frame", cv2.flip(frame, 1))
                cv2.imshow("mask", cv2.flip(mask, 1))
            if cv2.waitKey(1) == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()

if __name__ == "__main__":
    detector = ObjectDetector()
    detector.run()
