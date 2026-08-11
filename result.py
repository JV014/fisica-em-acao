import pygame
from settings import *

class Result:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 44, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen, score):
        # Removido o screen.fill para aparecer a estrada/paisagem ao fundo

        panel = pygame.Rect(120, 80, 760, 420)
        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel, 3, border_radius=15)

        title = self.title_font.render("FIM DA CAMPANHA!", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        score_text = self.title_font.render(f"Pontuação Final: {score} pontos", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 220))

        msg = self.text_font.render("Show, você concluiu a campanha! Reflita se precisa de mais prática.", True, (200, 220, 255))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 310))

        footer = self.small_font.render("Pressione ENTER para retornar ao Menu Principal", True, YELLOW)
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, 420))