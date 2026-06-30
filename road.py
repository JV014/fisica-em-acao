import pygame
from settings import *
from tree import Tree

class Road:

    def __init__(self):

        # Estrada
        self.road_y = 320
        self.road_height = 100

        self.level = "easy"

        # Grama
        self.grass_y = 420

        # Faixas
        self.line_y = 365
        self.line_width = 50
        self.line_height = 10
        self.line_spacing = 100
        self.number_of_lines = 12

        # Sol
        self.sun_x = 950
        self.sun_y = 70
        self.sun_radius = 35

    def draw(self, screen):

        self.draw_sky(screen)
        self.draw_sun(screen)
        self.draw_cloud(screen, 150, 80)
        self.draw_cloud(screen, 500, 120)
        self.draw_cloud(screen, 800, 70)

        self.draw_grass(screen)
        self.draw_trees(screen)

        self.draw_road(screen)
        self.draw_lines(screen)

    # =====================================
    # CÉU
    # =====================================

    def draw_sky(self, screen):
        if self.level == "easy":
            screen.fill((135, 206, 235))  # Céu azul claro
        elif self.level == "medium":
            screen.fill((225, 170, 80))  # Céu azul médio
        elif self.level == "hard":
            screen.fill((20, 30, 70))  # Céu azul escuro
        

    # =====================================
    # SOL e LUA 
    # =====================================

    def draw_sun(self, screen):
        if self.level == "easy":
            pygame.draw.circle(screen, YELLOW, (self.sun_x, self.sun_y), self.sun_radius)    # Sol amarelo
        elif self.level == "medium":
            pygame.draw.circle(screen, (255, 165, 0), (self.sun_x, self.sun_y), self.sun_radius)  # Sol laranja
        elif self.level == "hard":
            pygame.draw.circle(screen, (255, 255, 255), (self.sun_x, self.sun_y), self.sun_radius)  # Lua branca
    

    # =====================================
    # NUVENS
    # =====================================

    def draw_cloud(self, screen, x, y):

        pygame.draw.circle(screen, WHITE, (x, y), 20)
        pygame.draw.circle(screen, WHITE, (x + 20, y - 10), 25)
        pygame.draw.circle(screen, WHITE, (x + 45, y), 20)
        pygame.draw.circle(screen, WHITE, (x + 20, y + 8), 22)

    #====================================
    # ESTRELAS
    #====================================
    def draw_stars(self, screen):
        if self.level == "hard":
            stars = [(100, 50), (200, 80), (300, 40), (400, 90), (500, 60), (600, 30), (700, 70), (800, 50), (900, 80)]
            for star in stars:
                pygame.draw.circle(screen, WHITE, star, 2)
    # =====================================
    # GRAMA
    # =====================================

    def draw_grass(self, screen):

        pygame.draw.rect(
            screen,
            GREEN,
            (
                0,
                self.grass_y,
                WIDTH,
                HEIGHT - self.grass_y
            )
        )

    # =====================================
    # ÁRVORES
    # =====================================

    def draw_tree(self, screen, x):

        # Tronco
        pygame.draw.rect(
            screen,
            (139, 69, 19),
            (x, 260, 20, 60)
        )

        # Copa
        pygame.draw.circle(screen, (34, 139, 34), (x + 10, 245), 30)
        pygame.draw.circle(screen, (50, 170, 50), (x - 10, 260), 25)
        pygame.draw.circle(screen, (50, 170, 50), (x + 30, 260), 25)

    def draw_trees(self, screen):

        self.trees=[Tree(100, 260), Tree(300, 260), Tree(500, 260), Tree(700, 260), Tree(900, 260)]
        for tree in self.trees:
            tree.draw(screen)

    # =====================================
    # ESTRADA
    # =====================================

    def draw_road(self, screen):

        pygame.draw.rect(
            screen,
            GRAY,
            (
                0,
                self.road_y,
                WIDTH,
                self.road_height
            )
        )

    # =====================================
    # FAIXAS
    # =====================================

    def draw_lines(self, screen):

        for i in range(self.number_of_lines):

            pygame.draw.rect(
                screen,
                YELLOW,
                (
                    i * self.line_spacing,
                    self.line_y,
                    self.line_width,
                    self.line_height
                )
            )