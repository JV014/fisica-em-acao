import pygame
from settings import *

class Feedback:

    def __init__(self):

        self.correct = False
        self.message = ""

        self.title_font = pygame.font.SysFont(
            "Arial",
            42,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "Arial",
            28
        )

    # ======================================
    # DEFINE O FEEDBACK
    # ======================================

    def set_feedback(self, correct):

        self.correct = correct

        if correct:

            self.message = (
                "Muito bem! Você acertou a questão."
                "Ganhou 10 pontos."
            )

        else:

            self.message = (
                "Resposta incorreta. Tente novamente."
                "Perdeu 5 pontos."
            )

    # ======================================
    # DESENHAR
    # ======================================

    def draw(self, screen):

        painel = pygame.Rect(
            120,
            80,
            760,
            420
        )

        pygame.draw.rect(
            screen,
            (35, 35, 35),
            painel,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            WHITE,
            painel,
            3,
            border_radius=15
        )

        # -------------------------
        # TÍTULO
        # -------------------------

        if self.correct:

            titulo = "RESPOSTA CORRETA!"

            cor = (0,255,0)

        else:

            titulo = "RESPOSTA INCORRETA!"

            cor = RED

        text = self.title_font.render(
            titulo,
            True,
            cor
        )

        screen.blit(text,(210,130))

        # -------------------------
        # MENSAGEM
        # -------------------------

        msg = self.text_font.render(
            self.message,
            True,
            WHITE
        )

        screen.blit(msg,(180,240))

        # -------------------------
        # ENTER
        # -------------------------

        enter = self.text_font.render(
            "Pressione ENTER para continuar",
            True,
            YELLOW
        )

        screen.blit(
            enter,
            (
                WIDTH//2-enter.get_width()//2,
                400
            )
        )