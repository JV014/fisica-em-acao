import pygame

class Car:

    def __init__(self, x, y, image):

        self.x = x
        self.y = y

        self.image = image

        self.vx = 0
        self.vy = 0

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self, screen):

        screen.blit(
            self.image,
            (self.x, self.y)
        )

    def move(self, dt):

        self.x += self.vx * dt
        self.y += self.vy * dt