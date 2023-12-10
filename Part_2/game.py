import cv2
import sys
import numpy as np
import random
import os

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_directory)

from utils import detect_color_object
from Part_2.car import Car
from Part_2.obstacle import Obstacle


class Game:
    def __init__(
        self, game_frame_width, game_frame_height, cap_width=320, cap_height=180
    ):
        """
        Initialize the game.

        Parameters:
        - cap_width: Width of the camera frame.
        - cap_height: Height of the camera frame.
        - game_frame_width: Width of the game frame.
        - game_frame_height: Height of the game frame.
        """
        self.cap_width = cap_width
        self.cap_height = cap_height
        self.game_frame_width = game_frame_width
        self.game_frame_height = game_frame_height
        self.car_y_pos = game_frame_height - (game_frame_height // 5)
        self.obstacle_height = game_frame_height // 12
        self.obstacle_width = game_frame_width // 6
        self.car = Car(
            posX=game_frame_width // 2,
            posY=self.car_y_pos,
            height=self.obstacle_height,
            width=self.obstacle_width,
            color=[0, 255, 0],
        )

    def run(self):
        cap = cv2.VideoCapture(0)

        car_y_pos = self.game_frame_height - (self.game_frame_height // 5)

        # Set the width and height properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        i = 1
        # create a black background for the game
        game_frame = np.zeros(
            (self.game_frame_height, self.game_frame_width, 3), dtype=np.uint8
        )
        posX = int(self.game_frame_width / 2)  # Initial X position for the car

        list_obstacles = []
        positions = [
            self.game_frame_width // 4,
            self.game_frame_width // 2,
            self.game_frame_width - self.game_frame_width // 4,
        ]
        obstacle_height = 0
        score = 0
        height = self.game_frame_height - 1

        # Make sure the car dowsn't go out of the frame
        right_margin = self.game_frame_width - (
            self.car.width // 2 + self.obstacle_width // 2
        )
        left_margin = 20
        obstacle_hit = False

        while True:
            ret, frame = cap.read()

            # Create a black background for the game
            game_frame = np.zeros(
                (self.game_frame_height, self.game_frame_width, 3), dtype=np.uint8
            )

            # Detect the color
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
                frame = cv2.flip(frame, 1)
                frame, mask, points = detect_color_object(frame, color, 20, 100, 100)
                # Create a black background for the game
                game_frame = np.zeros(
                    (self.game_frame_height, self.game_frame_width, 3), dtype=np.uint8
                )
                cv2.flip(game_frame, 1)
                # Extract the Object position
                target_x = points[0][0]

                if points[0][0] != 0:
                    # Display a circle around the detected object
                    # Update car position based on the detected object
                    cv2.circle(frame, points[0], 10, (0, 255, 0), 2)
                    # PosX is the center of the car
                    posX = int(target_x * self.game_frame_width / self.cap_width)
                    # handle the delay with the car
                    car_pos = int(posX + self.car.width / 2)
                    # handle the delay between the frame and the game_frame
                    car_pos = int(car_pos * 0.8 + self.car.posX * 0.2)
                    previous_car_pos = car_pos

                else:
                    # Display a message if no object is detected
                    cv2.putText(
                        frame,
                        "No object detected",
                        (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    car_pos = previous_car_pos
                    # Keyboard controls
                    key = cv2.waitKeyEx(1)
                    if key == 2424832:
                        car_pos -= 10
                    elif key == 2555904:
                        car_pos += 10
                    previous_car_pos = car_pos

                # Draw the car
                self.car.draw(game_frame, car_pos)

                # Ensure the car stays within the frame margins
                car_pos = max(left_margin, car_pos + self.cap_width)
                # mark the right margin with red border
                car_pos = min(right_margin, car_pos)
                # Mark the left margin with red border

                # if there is no obstacle we create a new one
                if len(list_obstacles) == 0:
                    obstacle = Obstacle(
                        len(list_obstacles),
                        positions,
                        height=self.obstacle_height,
                        width=self.obstacle_width,
                    )
                    list_obstacles.append(obstacle)

                # Create obstacles and move them
                if obstacle_height > height:
                    obstacle = Obstacle(
                        len(list_obstacles),
                        positions,
                        height=self.obstacle_height,
                        width=self.obstacle_width,
                    )
                    list_obstacles.append(obstacle)
                    obstacle_height = 0
                    # add to the height progressively
                    if score % 2 == 0:
                        height -= 10
                # Move the obstacles
                # Check for collisions with the car
                for obstacle in list_obstacles:
                    obstacle_height = obstacle.move()
                    game_frame = obstacle.draw(game_frame)

                    if obstacle.is_hit(posX, car_y_pos):
                        obstacle_hit = True
                        list_obstacles = []
                        obstacle_height = 0
                        break

                for obstacle in list_obstacles:
                    if obstacle.is_out(self.game_frame_height):
                        list_obstacles.pop(0)
                        score += len(list_obstacles)
                # Display the score in the top left corner
                cv2.putText(
                    game_frame,
                    f"Score: {score}",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2,
                )

                cv2.imshow("frame", frame)
                cv2.imshow("game_frame", game_frame)

            if obstacle_hit:
                cv2.putText(
                    game_frame,
                    "Game Over",
                    (self.game_frame_width // 2 - 100, self.game_frame_height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
                # Your score is: {score}
                cv2.putText(
                    game_frame,
                    f"Your score is: {score}",
                    (
                        self.game_frame_width // 2 - 100,
                        self.game_frame_height // 2 + 50,
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2,
                )
                cv2.imshow("game_frame", game_frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


# if __name__ == "__main__":
#     game = Game(
#         cap_width=320, cap_height=180, game_frame_width=300, game_frame_height=540
#     )
#     game.run()
