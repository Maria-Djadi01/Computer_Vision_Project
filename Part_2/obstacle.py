import cv2
import random

class Obstacle:
    def __init__(self, id, Xpositions, Ypos=0, height=20, width=20, color=[0, 0, 255]):
        self.id = id
        self.Xpos = random.choice(Xpositions)
        self.Ypos = Ypos
        self.height = height
        self.width = width
        self.color = color

    def move(self, step=20):
        self.Ypos += step
        return self.Ypos

    def draw(self, img):
        img[self.Ypos - self.height:self.Ypos, self.Xpos - self.width:self.Xpos] = self.color
        return img

    def is_out(self, height):
        return self.Ypos > height

    def is_hit(self, x, y):
        return self.Xpos - self.width <= x <= self.Xpos + self.width and self.Ypos - self.height <= y <= self.Ypos
    
    def is_out(self, height):
        return self.Ypos > height