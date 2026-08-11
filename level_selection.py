import pygame
from settings import *

class LevelSelection:
    def __init__(self):
        self.options = [
            "9º Ano (Ensino Fundamental)",
            "Ensino Médio"
        ]
        self.selected = 0
        
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.option_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 16)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                # Retorna o nível escolhido: 'fundamental' (9º ano) ou 'medio' (Ensino Médio)
                return "fundamental" if self.selected == 0 else "medio"
        return None

    def draw(self, screen):
        # Caixa central do painel
        panel = pygame.Rect(120, 80, 760, 420)
        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, YELLOW, panel, 3, border_radius=15)

        title = self.title_font.render("SELECIONE O NÍVEL DE ENSINO", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        subtitle = self.info_font.render("Escolha o nível de dificuldade adequado para a sua turma:", True, WHITE)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 175))

        # Opções de escolha
        y = 250
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else WHITE
            text_str = f"►  {option}  ◄" if i == self.selected else f"    {option}    "
            
            opt_render = self.option_font.render(text_str, True, color)
            screen.blit(opt_render, (WIDTH // 2 - opt_render.get_width() // 2, y))
            y += 70

        footer = self.info_font.render("Use [↑ / ↓] para navegar e [ENTER] para confirmar", True, (200, 200, 200))
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, 435))