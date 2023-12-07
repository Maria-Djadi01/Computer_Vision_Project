import cv2
import sys
import numpy as np
import random

sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")

from utils import detect_color_object

class Obstacle:
    def __init__(self, id, Xpositions, Ypos):
        self.id = id
        self.Xpos = random.choice(Xpositions)
        self.Ypos = Ypos

    def move(self, step):
        self.Ypos += step
        return self.Ypos

    def draw(self, img, w, h, B, G, R):
        img[self.Ypos - h:self.Ypos, self.Xpos - w:self.Xpos] = [B, G, R]
        return img

    def is_out(self, height):
        return self.Ypos > height

    def is_hit(self, x, y, w, h):
        return self.Xpos - w < x < self.Xpos + w and self.Ypos - h < y < self.Ypos + h

def display_car(img, x, y, B, G, R):
    # the width and height of the car
    w = 50
    h = 20
    # color the pixels of the car
    img[y - h:y, x - w:x] = [B, G, R]
    return img

# Open the camera
cap = cv2.VideoCapture(0)

# Specify the desired width and height
desired_width = 640
desired_height = 480

# Set the width and height properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# get the width and the height of the frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width, height)

i = 1

# create a black background for the game
game_frame = np.zeros((desired_height, desired_width, 3), dtype=np.uint8)
posX = int(desired_width / 2)  # Initial X position for the car

list_obstacles = []
positions = [106, 319, 532]
obstacle_height = 0

while True:
    ret, frame = cap.read()

    # Create a black background for the game
    game_frame = np.zeros((desired_height, desired_width, 3), dtype=np.uint8)

    if i <= 100:
        x = int(desired_width / 4)
        y = int(desired_height / 2)
        cv2.circle(frame, (x, y), 5, (0, 255, 0), 2)
        b, g, r = tuple(frame[y, x])
        cv2.imshow("frame", cv2.flip(frame, 1))
        i += 1
        color = b, g, r
    else:
        frame, mask, points = detect_color_object(frame, color, 20, 100, 100)

        if len(points) > 0:
            cv2.circle(frame, points[0], 10, (0, 255, 0), 2)

            # Update car position based on the color object position
            target_x = points[0][0]
            posX += int((target_x - posX) * 0.1)  # Adjust the factor for smooth movement

            # Ensure the car stays within the frame
            posX = max(0, min(posX, width - 1))

            y = 400
            
            # Create a black background for the game
            game_frame = np.zeros((desired_height, desired_width, 3), dtype=np.uint8)
            
            # if there is no obstacle we create a new one
            if len(list_obstacles) == 0:
                obstacle = Obstacle(len(list_obstacles), positions, 0)
                list_obstacles.append(obstacle)
            # Create obstacles each time the last one is out of the frame
            if obstacle_height > height:
                obstacle = Obstacle(len(list_obstacles), positions, 0)
                list_obstacles.append(obstacle)
                obstacle_height = 0
            
            # Move the obstacles
            for obstacle in list_obstacles:
                obstacle_height = obstacle.move(20)

            # Draw the obstacles
            for obstacle in list_obstacles:
                game_frame = obstacle.draw(game_frame, 20, 20, 0, 0, 255)
                if obstacle.is_hit(posX, 200, 20, 20):
                    print("Game Over")
                    list_obstacles = []
                    obstacle_height = 0
                    break
            
            # Draw the car
            game_frame = display_car(game_frame, posX, y, 0, 255, 0)

            cv2.imshow("frame", cv2.flip(frame, 1))
            cv2.imshow("game_frame", cv2.flip(game_frame, 1))
            cv2.imshow("mask", cv2.flip(mask, 1))

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
