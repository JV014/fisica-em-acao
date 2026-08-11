import pygame
import math
import random
from settings import *

class TargetChallenge:
    def __init__(self):
        self.v0 = 15.0
        self.angle = 30.0
        self.g = 9.8
        
        self.projectile_fired = False
        self.x = 0.0
        self.y = 0.0
        self.time = 0.0
        self.path_points = []
        
        self.origin_x = 80
        self.origin_y = 450
        self.scale = 2.5 
        
        self.campaign_mode = False
        
        self.targets = [150.0, 80.0, 220.0, 50.0, 180.0]
        self.current_target_index = 0
        
        self.target_distance = self.targets[self.current_target_index]
        self.target_radius = 4.0 
        self.hit = False
        self.all_completed = False
        
        self.score = 0
        self.score_added = False
        
        # Controle de tentativas ajustado para 2 chances
        self.max_attempts = 2
        self.attempts_left = 2
        
        self.font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.success_font = pygame.font.SysFont("Arial", 36, bold=True)

    def set_mode(self, is_campaign=False):
        self.campaign_mode = is_campaign
        self.current_target_index = 0
        self.score = 0
        self.all_completed = False
        self.hit = False
        self.score_added = False
        self.attempts_left = 2 # Garante 2 tentativas ao iniciar
        
        if self.campaign_mode:
            self.target_distance = 150.0  
        else:
            self.target_distance = self.targets[0]
        self.reset_projectile()

    def reset_projectile(self):
        self.projectile_fired = False
        self.x = 0.0
        self.y = 0.0
        self.time = 0.0
        self.path_points = []
        self.hit = False

    def update(self, dt):
        if self.projectile_fired and not self.all_completed:
            self.time += dt 
            rad = math.radians(self.angle)
            
            vx = self.v0 * math.cos(rad)
            vy = self.v0 * math.sin(rad)
            
            self.x = vx * self.time
            self.y = (vy * self.time) - (0.5 * self.g * (self.time ** 2))
            
            screen_x = self.origin_x + int(self.x * self.scale)
            screen_y = self.origin_y - int(self.y * self.scale)
            self.path_points.append((screen_x, screen_y))
            
            if self.y <= 0 and self.time > 0.1:
                self.y = 0
                self.projectile_fired = False
                
                distance_error = abs(self.x - self.target_distance)
                if distance_error <= self.target_radius:
                    self.hit = True
                    if self.campaign_mode:
                        self.score = 100
                    else:
                        if distance_error <= 1.5:
                            self.score += 100 
                        else:
                            self.score += 50  
                else:
                    # Se errou, consome uma tentativa (tanto no isolado quanto na campanha)
                    self.attempts_left -= 1
                    if self.attempts_left <= 0:
                        self.all_completed = True # Acabaram as 2 tentativas

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.all_completed:
                if not self.hit: 
                    if event.key == pygame.K_RIGHT:
                        self.v0 = min(50.0, self.v0 + 1.0)
                    elif event.key == pygame.K_LEFT:
                        self.v0 = max(5.0, self.v0 - 1.0)
                    elif event.key == pygame.K_UP:
                        self.angle = min(85.0, self.angle + 1.0)
                    elif event.key == pygame.K_DOWN:
                        self.angle = max(5.0, self.angle - 1.0)
                    elif event.key == pygame.K_SPACE:
                        if not self.projectile_fired and self.attempts_left > 0:
                            self.reset_projectile()
                            self.projectile_fired = True
                else:
                    if event.key == pygame.K_RETURN:
                        if self.campaign_mode:
                            self.all_completed = True
                        else:
                            self.current_target_index += 1
                            if self.current_target_index < len(self.targets):
                                self.target_distance = self.targets[self.current_target_index]
                                self.attempts_left = 2 # Renova as 2 tentativas para o próximo alvo do modo isolado
                                self.reset_projectile()
                            else:
                                self.all_completed = True
            else:
                # Se acabou as tentativas ou o desafio, permite reiniciar com R (modo isolado)
                if event.key == pygame.K_r and not self.campaign_mode:
                    self.set_mode(is_campaign=False)

    def draw(self, screen):
        screen.fill((230, 245, 255))
        
        pygame.draw.rect(screen, GREEN, (0, self.origin_y, WIDTH, HEIGHT - self.origin_y))
        
        if not self.all_completed:
            target_px = self.origin_x + int(self.target_distance * self.scale)
            target_width = int(self.target_radius * 2 * self.scale)
            pygame.draw.rect(screen, RED, (target_px - target_width//2, self.origin_y - 5, target_width, 10))
            pygame.draw.circle(screen, YELLOW, (target_px, self.origin_y), 5)
        
        if len(self.path_points) > 1:
            pygame.draw.aalines(screen, BLUE, False, self.path_points)
            
        pygame.draw.circle(screen, (70, 70, 70), (self.origin_x, self.origin_y - 10), 12)
        rad = math.radians(self.angle)
        end_cx = self.origin_x + int(30 * math.cos(rad))
        end_cy = (self.origin_y - 10) - int(30 * math.sin(rad))
        pygame.draw.line(screen, BLACK, (self.origin_x, self.origin_y - 10), (end_cx, end_cy), 6)
        
        if self.projectile_fired or len(self.path_points) > 0:
            cur_sx = self.origin_x + int(self.x * self.scale)
            cur_sy = self.origin_y - int(self.y * self.scale)
            pygame.draw.circle(screen, BLACK, (cur_sx, cur_sy), 6)
            
        panel = pygame.Rect(WIDTH//2 - 380, 20, 760, 100)
        pygame.draw.rect(screen, (30, 35, 45), panel, border_radius=10)
        pygame.draw.rect(screen, YELLOW, panel, 2, border_radius=10)
        
        if self.campaign_mode:
            title = self.title_font.render(f"MISSÃO FINAL: TIRO AO ALVO (Tentativas: {self.attempts_left}/2)", True, YELLOW)
        else:
            title = self.title_font.render(f"DESAFIO TIRO AO ALVO (Fase {self.current_target_index + 1}/5) - [Tentativas: {self.attempts_left}/2]", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        if not self.all_completed:
            inst = self.font.render(f"Ajuste velocidade e ângulo para atingir o alvo a {self.target_distance} metros. | Pontos: {self.score}", True, WHITE)
            screen.blit(inst, (WIDTH//2 - inst.get_width()//2, 70))
        
        dash = pygame.Rect(20, 480, WIDTH - 40, 100)
        pygame.draw.rect(screen, (30, 35, 45), dash, border_radius=12)
        pygame.draw.rect(screen, WHITE, dash, 2, border_radius=12)
        
        control_txt = self.font.render(f"Velocidade Inicial: {self.v0:.1f} m/s (←/→)   |   Ângulo: {self.angle:.1f}° (↑/↓)", True, YELLOW)
        screen.blit(control_txt, (50, 500))
        
        tel_txt = self.font.render(f"Distância do último tiro: {self.x:.1f} m   |   Lançar [ESPAÇO]", True, WHITE)
        screen.blit(tel_txt, (50, 535))
        
        if self.hit and not self.all_completed:
            win_bg = pygame.Rect(WIDTH//2 - 250, 180, 500, 140)
            pygame.draw.rect(screen, (0, 130, 0), win_bg, border_radius=15)
            pygame.draw.rect(screen, WHITE, win_bg, 3, border_radius=15)
            
            win_text1 = self.success_font.render("ALVO ATINGIDO!", True, YELLOW)
            if self.campaign_mode:
                win_text2 = self.font.render("Pressione [ENTER] para ver seu resultado", True, WHITE)
            else:
                win_text2 = self.font.render("Pressione [ENTER] para o próximo desafio", True, WHITE)
            
            screen.blit(win_text1, (WIDTH//2 - win_text1.get_width()//2, 205))
            screen.blit(win_text2, (WIDTH//2 - win_text2.get_width()//2, 260))

        if self.all_completed:
            end_bg = pygame.Rect(WIDTH//2 - 280, 150, 560, 220)
            pygame.draw.rect(screen, (20, 40, 100), end_bg, border_radius=15)
            pygame.draw.rect(screen, YELLOW, end_bg, 3, border_radius=15)
            
            if self.attempts_left <= 0 and not self.hit:
                end_t1 = self.success_font.render("FIM DAS TENTATIVAS!", True, (255, 100, 100))
                if self.campaign_mode:
                    end_t2 = self.font.render("Você esgotou suas 2 tentativas na campanha.", True, WHITE)
                else:
                    end_t2 = self.font.render("Suas 2 tentativas acabaram! Pressione [R] para tentar.", True, WHITE)
            else:
                end_t1 = self.success_font.render("PARABÉNS!", True, YELLOW)
                if self.campaign_mode:
                    end_t2 = self.font.render("Você concluiu a campanha com sucesso!", True, WHITE)
                else:
                    end_t2 = self.font.render(f"Pontuação Total nos Desafios: {self.score} pts", True, WHITE)
            
            end_t3 = self.font.render("Pressione [ENTER] ou [ESC] para continuar", True, YELLOW)
            
            screen.blit(end_t1, (WIDTH//2 - end_t1.get_width()//2, 175))
            screen.blit(end_t2, (WIDTH//2 - end_t2.get_width()//2, 235))
            screen.blit(end_t3, (WIDTH//2 - end_t3.get_width()//2, 290))