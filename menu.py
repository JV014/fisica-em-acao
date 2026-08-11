import pygame
import math
from settings import *

class Menu:
    def __init__(self):
        self.options = [
            "Jogar Campanha",
            "Jogar Campanha Multiplayer",
            "Laboratório de Lançamento",
            "Desafio Tiro ao Alvo",
            "Créditos",
            "Sair"
        ]

        self.selected = 0

        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 20)
        self.menu_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.footer_font = pygame.font.SysFont("Arial", 16)

    def draw(self, screen):
        # ==========================================
        # 1. PAISAGEM DE FUNDO (Modo Tarde / Entardecer)
        # ==========================================
        screen.fill((225, 170, 80)) # Céu alaranjado
        
        # Sol Poente decorativo
        pygame.draw.circle(screen, (255, 215, 0), (820, 100), 40)
        
        # Chão / Grama
        ground_y = 420
        pygame.draw.rect(screen, (34, 120, 34), (0, ground_y, WIDTH, HEIGHT - ground_y))
        pygame.draw.line(screen, (20, 90, 20), (0, ground_y), (WIDTH, ground_y), 4)

        # ==========================================
        # 2. ELEMENTOS DECORATIVOS (Canhão e Parábola no Fundo)
        # ==========================================
        # Canhão decorativo no canto inferior esquerdo
        cannon_x, cannon_y = 120, ground_y - 5
        pygame.draw.circle(screen, (50, 50, 50), (cannon_x, cannon_y), 12) # Roda
        pygame.draw.line(screen, (90, 50, 30), (cannon_x, cannon_y), (cannon_x + 35, cannon_y - 25), 12) # Cano
        pygame.draw.circle(screen, BLACK, (cannon_x + 35, cannon_y - 25), 7) # Bala

        # Alvo decorativo no canto inferior direito
        target_x = 880
        pygame.draw.circle(screen, RED, (target_x, ground_y), 15)
        pygame.draw.circle(screen, WHITE, (target_x, ground_y), 9)
        pygame.draw.circle(screen, RED, (target_x, ground_y), 4)

        # ==========================================
        # 3. TÍTULO E SUBTÍTULO DO JOGO
        # ==========================================
        title = self.title_font.render("FÍSICA EM AÇÃO", True, (40, 30, 20))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        subtitle = self.subtitle_font.render("Cinemática e Investigação Científica", True, (70, 50, 30))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width()// 2, 95))

        # ==========================================
        # 4. CAIXA DE OPÇÕES DO MENU
        # ==========================================
        box_width = 460
        box_height = 280
        box_x = WIDTH // 2 - box_width // 2
        box_y = 135

        # Fundo semitransparente para as opções ficarem legíveis na paisagem
        s = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        s.fill((40, 30, 20, 220)) # Marrom escuro translúcido
        screen.blit(s, (box_x, box_y))
        pygame.draw.rect(screen, YELLOW, (box_x, box_y, box_width, box_height), 2, border_radius=8)

        # Renderização dos itens do menu
        y = box_y + 15
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else WHITE
            text_str = f"►  {option}  ◄" if i == self.selected else f"    {option}    "

            text = self.menu_font.render(text_str, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 42

        # ==========================================
        # 5. RODAPÉ DE INSTRUÇÃO
        # ==========================================
        footer = self.footer_font.render("Use as setas [↑ / ↓] para navegar e [ENTER] para selecionar", True, (255, 255, 255))
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, 535))