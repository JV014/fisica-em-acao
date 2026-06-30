import pygame
from settings import *

class Phase:

    def __init__(self):

        self.title_font = pygame.font.SysFont(
            "Arial",
            42,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "Arial",
            28
        )

        self.phase = 1

    def set_phase(self, phase):

        self.phase = phase

    def draw(self, screen):

        painel = pygame.Rect(100,80, 800, 440)
        pygame.draw.rect(
            screen, (35, 35, 35), painel, border_radius=20)
           

        pygame.draw.rect(
                screen, WHITE, painel, 3, border_radius=20)


        if self.phase == 2:

            titulo = "🌅 FASE 2"

            texto = [

                "Parabéns!",

                "Agora você estudará",

                "Movimento Uniformemente Variado.",

                "",

                "A partir daqui",

                "entraremos no conceito",

                "de aceleração.",

                "",

                "Pressione ENTER."
            ]

        elif self.phase == 3:

            titulo = "🌙 FASE 3"

            texto = [

                "Excelente!",

                "Agora começam",

                "os desafios avançados.",

                "",

                "Você utilizará",

                "as equações do MUV.",

                "",

                "Pressione ENTER."
            ]

        else:

            return

        render = self.title_font.render(

            titulo,

            True,

            YELLOW

        )

        screen.blit(

            render,

            (WIDTH//2-render.get_width()//2,80)

        )

        y = 170

        for linha in texto:

            txt = self.text_font.render(

                linha,

                True,

                WHITE

            )

            screen.blit(

                txt,

                (WIDTH//2-txt.get_width()//2,y)

            )

            y += 40