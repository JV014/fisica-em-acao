import pygame

BROWN = (139,69,19)

GREEN1 = (34,139,34)

GREEN2 = (50,170,50)


class Tree:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def draw(self, screen):

        # Tronco

        pygame.draw.rect(

            screen,

            BROWN,

            (self.x, self.y, 20, 60)

        )

        pygame.draw.circle(

            screen,

            GREEN1,

            (self.x+10, self.y-15),

            30

        )

        pygame.draw.circle(

            screen,

            GREEN2,

            (self.x-10, self.y),

            25

        )

        pygame.draw.circle(

            screen,

            GREEN2,

            (self.x+30, self.y),

            25

        )