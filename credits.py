import pygame
from settings import *

class Credits:

    def __init__(self):

        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

    def draw(self, screen):

        screen.fill((20, 40, 100))

        panel = pygame.Rect(120, 50, 760, 500)

        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel, 3, border_radius=15)

        titulo = self.title_font.render(
            "CRÉDITOS",
            True,
            YELLOW
        )

        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 80))

        textos = [

            "Desenvolvimento",
            "João Vitor da Silva Souza",

            "",
            "Mestrando em Ciência dos Materiais (UNIVASF)",
            "Graduado em Física (IFsertãoPE)"

            "",

            "Tecnologias",
            "Python",
            "Pygame",

            "",

            "Versão 1.0 - 2026"

        ]

        y = 170

        for linha in textos:

            texto = self.text_font.render(
                linha,
                True,
                WHITE
            )

            screen.blit(
                texto,
                (WIDTH//2 - texto.get_width()//2, y)
            )

            y += 35

        voltar = self.small_font.render(
            "Pressione ENTER para voltar ao menu",
            True,
            YELLOW
        )

        screen.blit(
            voltar,
            (WIDTH//2 - voltar.get_width()//2, 520)
        )