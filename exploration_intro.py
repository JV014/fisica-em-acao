import pygame
from settings import *

class ExplorationIntro:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 44, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen):
        panel = pygame.Rect(120, 50, 760, 460)
        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel, 3, border_radius=15)

        title = self.title_font.render("LABORATÓRIO DE LANÇAMENTO", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        textos = [
            "Explore o Lançamento de Projéteis alterando variáveis físicas.",
            "",
            "Comandos:",
            "  • Ajustar Velocidade: Setas [←] / [→]",
            "  • Ajustar Ângulo: Setas [↑] / [↓]",
            "  • Lançar Projétil: Tecla [ESPAÇO]",
            "  • Trocar de Planeta (Gravidade): Tecla [P]",
            "  • Alternar Vetores [V] e Trajetória [T]"
        ]

        y = 170
        for linha in textos:
            texto = self.text_font.render(linha, True, WHITE)
            screen.blit(texto, (170, y))
            y = y + 32 if linha != "" else y + 15

        enter = self.small_font.render("Pressione ENTER para entrar no laboratório", True, YELLOW)
        screen.blit(enter, (WIDTH//2 - enter.get_width()//2, 460))