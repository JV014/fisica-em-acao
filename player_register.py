import pygame
from settings import *

class PlayerRegister:
    def __init__(self):
        self.name = ""
        self.max_chars = 22
        self.title_font = pygame.font.SysFont("Arial", 34, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 20)
        self.input_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 16)

    def reset(self):
        self.name = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self.name.strip()) > 0:
                    return self.name.strip()
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            else:
                if len(self.name) < self.max_chars and event.unicode.isprintable():
                    self.name += event.unicode
        return None

    def draw(self, screen, prompt_title="BEM-VINDO AO FÍSICA EM AÇÃO 3.0", prompt_sub="Digite seu nome para registrar sua participação:"):
        screen.fill((225, 170, 80))
        ground_y = 420
        pygame.draw.rect(screen, (34, 120, 34), (0, ground_y, WIDTH, HEIGHT - ground_y))

        panel = pygame.Rect(WIDTH // 2 - 360, 110, 720, 360)
        pygame.draw.rect(screen, (35, 30, 25), panel, border_radius=15)
        pygame.draw.rect(screen, YELLOW, panel, 3, border_radius=15)

        title = self.title_font.render(prompt_title, True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 145))

        sub = self.subtitle_font.render(prompt_sub, True, WHITE)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 210))

        input_box = pygame.Rect(WIDTH // 2 - 220, 265, 440, 55)
        pygame.draw.rect(screen, (20, 20, 25), input_box, border_radius=8)
        pygame.draw.rect(screen, (100, 200, 255), input_box, 2, border_radius=8)

        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        txt_surface = self.input_font.render(self.name + cursor, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 15, input_box.y + 12))

        hint = self.info_font.render("Pressione [ENTER] para confirmar e continuar", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 365))