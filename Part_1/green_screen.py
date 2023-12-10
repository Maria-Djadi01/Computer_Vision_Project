import cv2
import sys
from PIL import Image
import os

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_directory)

from utils import (
    get_limits,
    BGR2HSV,
    my_inRange,
    green_screen,
    BGR2HSV_color,
    my_copy,
    my_shape,
)


class GreenScreen:
    def __init__(self, background):
        """
        Initialize the GreenScreen object.

        Parameters:
        - background: Path to the background image.
        """
        self.background = background
        self.color = None
        self.mask = None
        self.result = None
        self.cap_width = 320
        self.cap_height = 180

    def green_screen(self, mask, img, back):
        """
        Apply green screen effect to an image.

        Parameters:
        - mask: Binary mask indicating the region to replace.
        - img: Input image.
        - back: Background image.

        Returns:
        - np.array: Resulting image with green screen effect applied.
        """
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

        # Load the background image
        back = cv2.imread(self.background)
        frame = cap.read()[1]
        back = cv2.resize(back, (my_shape(frame, gray=False)[1], my_shape(frame, gray=False)[0]))

        i = 1
        while True:
            ret, frame = cap.read()
            if i <= 200:
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
                    f"Clear the screen to detect the color of the background",
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
                hsv_color = BGR2HSV_color(color)
                hsv_img = BGR2HSV(frame)
                lower_b, upper_b = get_limits(hsv_color, 20, 100, 100)
                mask = my_inRange(hsv_img, lower_b, upper_b)
                # Apply green screen effect
                result = self.green_screen(mask, frame, back)
                # Display frames
                cv2.imshow("frame", cv2.flip(frame, 1))
                cv2.imshow("mask", cv2.flip(mask, 1))
                cv2.imshow("result", cv2.flip(result, 1))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
