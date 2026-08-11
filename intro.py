import pygame
from settings import *

class Intro:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 44, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 18)
        self.small_font = pygame.font.SysFont("Arial", 18)

    def draw(self, screen):
        panel = pygame.Rect(120, 45, 760, 510)
        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel, 3, border_radius=15)

        title = self.title_font.render("Seja bem-vindo!", True, YELLOW)
        screen.blit(title, (160, 65))

        textos = [
            "Olá, seja bem-vindo ao Modo Campanha Individual de Cinemática!",

            "Esse jogo tem como objetivo explorar os conceitos de Cinemática: MU e MUV.",
            "No caso de alunos de Ensino médio, o jogo oferece desafios mais avançados",
            "incluindo o Lançamento de Projéteis e Tiro ao Alvo.",
            "O jogo é dividido em 5 fases:",
            "Fase 1: Conceitos Básicos de Cinemática (Ensino Fundamental e Médio)",
            "Fase 2: Cinemática de Movimento Uniforme (Ensino Fundamental e Médio)",
            "Fase 3: Cinemática de Movimento Unif. Variado (Ensino Fundamental e Médio)",
            "Fase 4: Lançamento de Projéteis (Ensino Médio)",
            "Fase 5: Tiro ao Alvo (Ensino Médio)",
            "Esperamos que você se divirta e aprenda bastante!"        ]
    

        y = 135
        for linha in textos:
            texto = self.text_font.render(linha, True, WHITE)
            screen.blit(texto, (160, y))
            y = y + 24 if any(k in linha for k in ["1.", "2.", "3.", "4.", "5.", "O jogo"]) else y + 22

        enter = self.small_font.render("Pressione ENTER para continuar", True, YELLOW)
        screen.blit(enter, (WIDTH // 2 - enter.get_width() // 2, 515))