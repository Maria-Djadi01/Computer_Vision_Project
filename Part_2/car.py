import cv2

class Car():
    def __init__(self, posX, posY, height=20, width=50, color=[0, 255, 0]):
        self.posX = posX
        self.posY = posY
        self.height = height
        self.width = width
        self.color = color

    def move(self, step=5):
        self.posY += step
        return self.posY

    def draw(self, img, posX):
        self.posX = posX
        img[self.posY - self.height:self.posY, self.posX - self.width:self.posX] = self.color
        return img

    def is_hit(self, x, y, w, h):
        return self.posX - w < x < self.posX + w and self.posY - h < y < self.posY + h