import pygame
from settings import *

class Intro:

    def __init__(self):

        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen):

        # Painel central
        panel = pygame.Rect(120, 50, 760, 460)

        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel, 3, border_radius=15)

        # Título
        title = self.title_font.render(
            "Seja bem-vindo!",
            True,
            YELLOW
        )

        screen.blit(title, (180, 80))

        textos = [

            "Esse jogo tem como objetivo ensinar os conceitos de",

            "Movimento Uniforme (MU) e Movimento Uniformemente Variado (MUV).",

            "Esperamos que você se divirta e aprenda bastante!",

            "",

            "O jogo é dividido em 3 fases:",
            "Fase 1: Movimento Uniforme (MU)",
            "Fase 2: Movimento Uniformemente Variado (MUV)",
            "Fase 3: Movimento Uniforme e Uniformemente Variado (MU e MUV)",


        ]

        y = 170

        enter = self.small_font.render(
            "Pressione ENTER para continuar",
            True,
            WHITE
        )
        screen.blit(enter, (WIDTH//2-enter.get_width()//2, 480))

        for linha in textos:

            texto = self.text_font.render(
                linha,
                True,
                WHITE
            )
    
            screen.blit(texto, (170, y))

            y += 32