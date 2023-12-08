import cv2
import sys
import numpy as np
import random

sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")

from utils import detect_color_object
from Part_2.car import Car
from Part_2.obstacle import Obstacle

class Game():
    def __init__(self, cap_width, cap_height, game_frame_width, game_frame_height):
        self.cap_width = cap_width
        self.cap_height = cap_height
        self.game_frame_width = game_frame_width
        self.game_frame_height = game_frame_height
        self.car_y_pos = game_frame_height - (game_frame_height // 5)
        self.car = Car(posX=game_frame_width // 2, posY=self.car_y_pos, height=game_frame_height // 10, width=game_frame_width // 5, color=[0, 255, 0])
        self.obstacle_height = game_frame_height // 10
        self.obstacle_width = game_frame_width // 5
    def run(self):
        cap = cv2.VideoCapture(0)

        car_y_pos = self.game_frame_height - (self.game_frame_height // 5)

        # Set the width and height properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        i = 1

        # create a black background for the game
        game_frame = np.zeros((self.game_frame_height, self.game_frame_width, 3), dtype=np.uint8)
        posX = int(self.game_frame_width / 2)  # Initial X position for the car

        list_obstacles = []
        positions = [self.game_frame_width // 4, self.game_frame_width // 2, self.game_frame_width - self.game_frame_width // 4]
        obstacle_height = 0
        score = 0
        height = 180

        # Make sure the car dowsn't go out of the frame
        left_margin = self.car.width // 2 + self.obstacle_width // 2
        right_margin = int(self.game_frame_width - self.car.width // 2 - 10)

        while True:
            ret, frame = cap.read()

            # Create a black background for the game
            game_frame = np.zeros((self.game_frame_height, self.game_frame_width, 3), dtype=np.uint8)

            if i <= 100:
                x = int(self.cap_width / 4)
                y = int(self.cap_height / 2)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), 2)
                b, g, r = tuple(frame[y, x])
                cv2.imshow("frame", cv2.flip(frame, 1))
                i += 1
                color = b, g, r
            else:
                frame, mask, points = detect_color_object(frame, color, 20, 100, 100)
                # Create a black background for the game
                game_frame = np.zeros((self.game_frame_height, self.game_frame_width, 3), dtype=np.uint8)
                # Object position
                target_x = points[0][0]

                if points[0][0] != 0:
                    cv2.circle(frame, points[0], 10, (0, 255, 0), 2)
                    # PosX is the center of the car
                    posX = int(target_x * self.game_frame_width / self.cap_width)
                    car_pos = int(posX + self.car.width / 2)
                    right_car = int(posX - self.car.width / 2)
                    previous_car_pos = car_pos
                
                elif previous_car_pos is not None:
                    car_pos = previous_car_pos
                else:
                    car_pos = int(self.cap_width / 2)
                    cv2.putText(frame, "No object detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                car_pos = max(left_margin, car_pos)
                car_pos = min(right_margin, car_pos)
                
                
                # Draw the car
                game_frame = self.car.draw(game_frame, car_pos)


                # if there is no obstacle we create a new one
                if len(list_obstacles) == 0:
                    obstacle = Obstacle(len(list_obstacles), positions, height=self.obstacle_height, width=self.obstacle_width)
                    list_obstacles.append(obstacle)
                
                # Create obstacles each time the last one reaches a certain height
                if obstacle_height > height:
                    obstacle = Obstacle(len(list_obstacles), positions, height=self.obstacle_height, width=self.obstacle_width)
                    list_obstacles.append(obstacle)
                    obstacle_height = 0
                    score += 1
                
                # Move the obstacles
                for obstacle in list_obstacles:
                    obstacle_height = obstacle.move()
                    game_frame = obstacle.draw(game_frame)

                    if obstacle.is_hit(posX, car_y_pos):
                        print("Game Over")
                        list_obstacles = []
                        obstacle_height = 0
                        break
                
                for obstacle in list_obstacles:
                    if obstacle.is_out(self.game_frame_height):
                        list_obstacles.pop(0)
                        score += len(list_obstacles)
                
                cv2.imshow("frame", cv2.flip(frame, 1))
                cv2.imshow("game_frame", cv2.flip(game_frame, 1))
                cv2.imshow("mask", cv2.flip(mask, 1))

            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = Game(cap_width=320, cap_height=180, game_frame_width=250, game_frame_height=540)
    game.run()
