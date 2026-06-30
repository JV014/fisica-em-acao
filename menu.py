import pygame
from settings import *

class Menu:

    def __init__(self):

        self.options = [

            "Iniciar",

            "Créditos",

            "Sair"

        ]

        self.selected = 0

        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)

        self.menu_font = pygame.font.SysFont("Arial", 36)

    def draw(self, screen):

        screen.fill((20, 40, 100))

        # Título
        title = self.title_font.render(
            "Física em Ação",
            True,
            WHITE
        )

        screen.blit(
            title,
            (
                WIDTH//2-title.get_width()//2,
                80
            )
        )

        subtitle = self.menu_font.render(
            "MU e MUV",
            True,
            WHITE
        )

        screen.blit(
            subtitle,
            (
                WIDTH//2-subtitle.get_width()//2,
                150
            )
        )

        y = 260

        for i, option in enumerate(self.options):

            color = YELLOW if i == self.selected else WHITE

            text = self.menu_font.render(
                option,
                True,
                color
            )

            screen.blit(
                text,
                (
                    WIDTH//2-text.get_width()//2,
                    y
                )
            )

            y += 60