import pygame
from settings import *

class MultiplayerIntro:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen):
        panel = pygame.Rect(120, 50, 760, 460)
        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel, 3, border_radius=15)

        title = self.title_font.render("MODO 2 PLAYERS", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        textos = [
            "Bem-vindos ao desafio competitivo de Cinemática!",
            "Joguem simultaneamente no mesmo teclado dividindo a tela.",
            "",
            "Controles do Jogador 1 (Esquerda - Azul):",
            "  • Navegar: Teclas [W] / [S]",
            "  • Confirmar resposta: Tecla [ENTER]",
            "",
            "Controles do Jogador 2 (Direita - Amarelo):",
            "  • Navegar: Setas [↑] / [↓]",
            "  • Confirmar resposta: Tecla [ESPAÇO]"
        ]

        y = 170
        for linha in textos:
            texto = self.text_font.render(linha, True, WHITE)
            screen.blit(texto, (170, y))
            y = y + 28 if linha != "" else y + 15

        enter = self.small_font.render("Pressione ENTER para iniciar a partida", True, YELLOW)
        screen.blit(enter, (WIDTH//2 - enter.get_width()//2, 460))