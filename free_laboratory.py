import pygame
import math
import random
from settings import *

class FreeLaboratory:
    def __init__(self):
        self.v0 = 20.0
        self.angle = 45.0
        self.g = 9.8
        self.planet_name = "Terra"
        
        self.projectile_fired = False
        self.x = 0.0
        self.y = 0.0
        self.time = 0.0
        self.path_points = []
        
        self.origin_x = 80
        self.origin_y = 450
        self.scale = 3.5
        
        self.show_trajectory = True
        self.show_vectors = True
        self.stars = [(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 150)) for _ in range(50)]

        self.tips = [
            "Dica: O alcance máximo no vácuo é obtido com o ângulo de 45°.",
            "Dica: A velocidade inicial (v0) e o ângulo de lançamento determinam a trajetória.",
            "Dica: A gravidade (g) afeta a altura máxima e o alcance do projétil.",
            "Dica: A massa do projétil não afeta sua trajetória em um vácuo.",
            "Dica: A resistência do ar não é considerada neste modelo.",
            "Dica: A trajetória de um projétil em um vácuo é sempre uma parábola.",
            "Dica: A velocidade horizontal (Vx) permanece constante durante o voo.",
            "Dica: A velocidade vertical (Vy) muda devido à gravidade.",
            "Dica: O tempo de voo depende da altura inicial e da velocidade vertical.",
            "Dica: No ponto de altura máxima, a velocidade vertical (Vy) é zero.",
            "Dica: Pressione [P] para testar a gravidade em outros planetas (Marte, Lua, Júpiter)."
        ]
        self.tip_index = 0

        self.font = pygame.font.SysFont("Arial", 16)
        self.bold_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 20, bold=True)

    def reset_projectile(self):
        self.projectile_fired = False
        self.x = 0.0
        self.y = 0.0
        self.time = 0.0
        self.path_points = []

    def update(self, dt):
        if self.projectile_fired:
            self.time += dt  # Tempo real sem distorções
            rad = math.radians(self.angle)
            
            vx = self.v0 * math.cos(rad)
            vy = self.v0 * math.sin(rad)
            
            # Física limpa e idêntica ao tiro ao alvo
            self.x = vx * self.time
            self.y = (vy * self.time) - (0.5 * self.g * (self.time ** 2))
            
            screen_x = self.origin_x + int(self.x * self.scale)
            screen_y = self.origin_y - int(self.y * self.scale)
            self.path_points.append((screen_x, screen_y))
            
            if self.y <= 0 and self.time > 0.1:
                self.y = 0
                self.projectile_fired = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.v0 = min(50.0, self.v0 + 1.0)
            elif event.key == pygame.K_LEFT:
                self.v0 = max(5.0, self.v0 - 1.0)
            elif event.key == pygame.K_UP:
                self.angle = min(85.0, self.angle + 1.0)
            elif event.key == pygame.K_DOWN:
                self.angle = max(5.0, self.angle - 1.0)
            elif event.key == pygame.K_SPACE:
                if not self.projectile_fired:
                    self.reset_projectile()
                    self.projectile_fired = True
            elif event.key == pygame.K_p:
                if self.planet_name == "Terra":
                    self.g = 3.7
                    self.planet_name = "Marte"
                elif self.planet_name == "Marte":
                    self.g = 1.6
                    self.planet_name = "Lua"
                elif self.planet_name == "Lua":
                    self.g = 24.8
                    self.planet_name = "Júpiter"
                else:
                    self.g = 9.8
                    self.planet_name = "Terra"
            elif event.key == pygame.K_v:
                self.show_vectors = not self.show_vectors
            elif event.key == pygame.K_t:
                self.show_trajectory = not self.show_trajectory
            elif event.key == pygame.K_RETURN:
                self.tip_index = (self.tip_index + 1) % len(self.tips)

    def draw(self, screen):
        if self.planet_name == "Terra":
            sky_color, ground_color, horizon_color = (135, 206, 235), (34, 139, 34), (0, 100, 0)
        elif self.planet_name == "Marte":
            sky_color, ground_color, horizon_color = (210, 105, 30), (139, 69, 19), (100, 40, 10)
        elif self.planet_name == "Lua":
            sky_color, ground_color, horizon_color = (10, 10, 20), (220, 220, 220), (150, 150, 150)
        else:
            sky_color, ground_color, horizon_color = (180, 140, 100), (110, 70, 40), (80, 40, 20)

        screen.fill(sky_color)
        if self.planet_name == "Lua":
            for sx, sy in self.stars:
                pygame.draw.circle(screen, WHITE, (sx, sy), 1)

        pygame.draw.rect(screen, ground_color, (0, self.origin_y, WIDTH, HEIGHT - self.origin_y))
        pygame.draw.line(screen, horizon_color, (0, self.origin_y), (WIDTH, self.origin_y), 4)

        rad = math.radians(self.angle)
        cannon_base_x, cannon_base_y = self.origin_x, self.origin_y - 10
        pygame.draw.circle(screen, (50, 50, 50), (cannon_base_x, cannon_base_y + 5), 14)
        
        cannon_len = 45
        end_cx = cannon_base_x + int(cannon_len * math.cos(rad))
        end_cy = cannon_base_y - int(cannon_len * math.sin(rad))
        pygame.draw.line(screen, (90, 50, 30), (cannon_base_x, cannon_base_y), (end_cx, end_cy), 12)
        
        if not self.projectile_fired and len(self.path_points) == 0:
            pygame.draw.circle(screen, BLACK, (end_cx, end_cy), 7)

        if self.show_trajectory and len(self.path_points) > 1:
            pygame.draw.aalines(screen, (20, 40, 120), False, self.path_points)

        if self.projectile_fired or len(self.path_points) > 0:
            cur_sx = self.origin_x + int(self.x * self.scale)
            cur_sy = self.origin_y - int(self.y * self.scale)
            pygame.draw.circle(screen, BLACK, (cur_sx, cur_sy), 6)

            if self.show_vectors:
                vx_inst = self.v0 * math.cos(rad)
                vy_inst = (self.v0 * math.sin(rad)) - (self.g * self.time)
                v_scale = 1.2
                vec_vx_len = int(vx_inst * v_scale)
                vec_vy_len = int(vy_inst * v_scale)

                pygame.draw.line(screen, WHITE, (cur_sx, cur_sy), (cur_sx + vec_vx_len, cur_sy), 2)
                pygame.draw.line(screen, RED, (cur_sx, cur_sy), (cur_sx, cur_sy - vec_vy_len), 2)

        panel = pygame.Rect(WIDTH - 540, 15, 520, 100)
        pygame.draw.rect(screen, (30, 35, 45), panel, border_radius=10)
        pygame.draw.rect(screen, YELLOW, panel, 2, border_radius=10)
        
        q_title = self.title_font.render("LABORATÓRIO DE LANÇAMENTO", True, YELLOW)
        screen.blit(q_title, (panel.x + 15, panel.y + 12))
        
        tip_text = self.font.render(self.tips[self.tip_index], True, WHITE)
        screen.blit(tip_text, (panel.x + 15, panel.y + 45))
        
        press_enter = self.font.render("Pressione [ENTER] para ver outra dica", True, (200, 200, 200))
        screen.blit(press_enter, (panel.x + 15, panel.y + 70))

        dash = pygame.Rect(20, 485, WIDTH - 40, 100)
        pygame.draw.rect(screen, (30, 35, 45), dash, border_radius=12)
        pygame.draw.rect(screen, WHITE, dash, 2, border_radius=12)
        
        control_txt = self.bold_font.render(f"Velocidade (v0): {self.v0:.1f} m/s (←/→)   |   Ângulo: {self.angle:.1f}° (↑/↓)", True, YELLOW)
        screen.blit(control_txt, (35, 500))
        
        vx_cur = self.v0 * math.cos(rad)
        vy_cur = (self.v0 * math.sin(rad)) - (self.g * self.time)
        v_total = math.sqrt(vx_cur**2 + vy_cur**2)
        
        info_txt1 = self.font.render(f"Tempo: {self.time:.2f}s  |  Altura: {max(0.0, self.y):.1f}m  |  Distância: {self.x:.1f}m  |  Vx: {vx_cur:.1f}m/s  |  Vy: {vy_cur:.1f}m/s  |  V: {v_total:.1f}m/s", True, WHITE)
        screen.blit(info_txt1, (35, 530))
        
        info_txt2 = self.font.render(f"Planeta: {self.planet_name} [P]  |  Vetores [V]  |  Trajetória [T]  |  Lançar [ESPAÇO]  |  Menu [ESC]", True, (200, 220, 255))
        screen.blit(info_txt2, (35, 555))