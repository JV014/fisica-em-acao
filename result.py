import pygame
from settings import *

class Result:

    def __init__(self):

        self.title = pygame.font.SysFont(
            "Arial",
            46,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "Arial",
            30
        )

    def draw(self, screen, score):

        screen.fill((20, 40, 100))

        txt = self.title.render(

            "MISSÃO CONCLUÍDA!",

            True,

            WHITE

        )

        screen.blit(

            txt,

            (
                WIDTH//2-txt.get_width()//2,
                100
            )
        )

        pts = self.font.render(

            f"Pontuação: {score}/150",

            True,

            YELLOW

        )

        screen.blit(

            pts,

            (
                WIDTH//2-pts.get_width()//2,
                220
            )
        )

        if score == 150:

            msg = "Excelente!"

        elif score >= 50:

            msg = "Muito bom!"

        elif score >= 100:

            msg = "Bom trabalho!"

        else:

            msg = "Continue estudando!"

        texto = self.font.render(

            msg,

            True,

            WHITE

        )

        screen.blit(

            texto,

            (
                WIDTH//2-texto.get_width()//2,
                320
            )
        )