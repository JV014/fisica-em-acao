import pygame
import math
from settings import *

class ExplorationMode:
    def __init__(self):
        self.v0, self.angle, self.g = 20.0, 45.0, 9.8
        self.projectile_fired = False
        self.x, self.y, self.time = 0.0, 0.0, 0.0
        self.path_points = []
        
        self.origin_x, self.origin_y = 100, 450
        self.scale = 3.5
        
        self.lab_questions = [
            {"question": "O que acontece com o alcance se aumentarmos o ângulo para 45°?", "options": ["A) Alcance máximo (vácuo).", "B) Alcance nulo.", "C) Altura diminui.", "D) Tempo não altera."], "correct": 0},
            {"question": "No ponto de altura máxima, qual componente da velocidade é zero?", "options": ["A) Horizontal (Vx).", "B) Vertical (Vy).", "C) Ambas.", "D) Nenhuma."], "correct": 1},
            {"question": "Como a gravidade afeta o tempo de voo do projétil?", "options": ["A) Maior gravidade aumenta o tempo.", "B) Maior gravidade diminui o tempo.", "C) Não afeta.", "D) O projétil viaja mais."], "correct": 1},
            {"question": "Se a velocidade inicial for dobrada, o alcance horizontal:", "options": ["A) Dobra.", "B) Reduz à metade.", "C) Mantém.", "D) Quadruplica."], "correct": 3},
            {"question": "Qual a relação entre o ângulo de lançamento e a altura máxima?", "options": ["A) A altura é independente do ângulo.", "B) A altura aumenta com o ângulo.", "C) A altura diminui.", "D) Máxima em 45°."], "correct": 1}
        ]
        self.lab_index = 0
        self.question_selected = 0
        
        self.font = pygame.font.SysFont("Arial", 16)
        self.bold_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 20, bold=True)

    def reset(self):
        """Reseta o laboratório para permitir jogar novamente sem erros"""
        self.lab_index = 0
        self.question_selected = 0
        self.v0 = 20.0
        self.angle = 45.0
        self.reset_projectile()

    def reset_projectile(self):
        self.projectile_fired = False
        self.time = 0.0
        self.path_points = []

    def update(self, dt):
        if self.projectile_fired:
            self.time += dt * 1.5
            rad = math.radians(self.angle)
            self.x = (self.v0 * math.cos(rad)) * self.time
            self.y = (self.v0 * math.sin(rad)) * self.time - (0.5 * self.g * (self.time**2))
            screen_x = self.origin_x + int(self.x * self.scale)
            screen_y = self.origin_y - int(self.y * self.scale)
            self.path_points.append((screen_x, screen_y))
            if self.y < 0: 
                self.projectile_fired = False

    def handle_event(self, event, question_obj, feedback_obj):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: 
                self.v0 = min(50.0, self.v0 + 1.0)
            elif event.key == pygame.K_LEFT: 
                self.v0 = max(5.0, self.v0 - 1.0)
            elif event.key == pygame.K_UP: 
                self.angle = min(85.0, self.angle + 1.0)
            elif event.key == pygame.K_DOWN: 
                self.angle = max(0.0, self.angle - 1.0)
            elif event.key == pygame.K_SPACE:
                if not self.projectile_fired: 
                    self.reset_projectile()
                    self.projectile_fired = True
            
            elif self.lab_index < len(self.lab_questions):
                current_opts = self.lab_questions[self.lab_index]["options"]
                if event.key == pygame.K_s: 
                    self.question_selected = (self.question_selected + 1) % len(current_opts)
                elif event.key == pygame.K_w: 
                    self.question_selected = (self.question_selected - 1) % len(current_opts)
                elif event.key == pygame.K_RETURN:
                    is_correct = (self.question_selected == self.lab_questions[self.lab_index]["correct"])
                    question_obj.update_score(is_correct)
                    feedback_obj.set_feedback(is_correct)
                    self.lab_index += 1
                    self.question_selected = 0
                    return True 
        return False

    def finished(self):
        return self.lab_index >= len(self.lab_questions)

    def draw(self, screen):
        # 1. Fundo padrão do jogo
        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (34, 139, 34), (0, 480, WIDTH, HEIGHT - 480))
        pygame.draw.rect(screen, (100, 100, 100), (0, 420, WIDTH, 60))
        pygame.draw.line(screen, YELLOW, (0, 450), (WIDTH, 450), 3)

        if len(self.path_points) > 1:
            pygame.draw.aalines(screen, (50, 50, 50), False, self.path_points)

        # 2. Canhão
        rad = math.radians(self.angle)
        cannon_len = 45
        end_x = self.origin_x + int(cannon_len * math.cos(rad))
        end_y = self.origin_y - int(cannon_len * math.sin(rad))
        pygame.draw.circle(screen, (60, 60, 60), (self.origin_x, self.origin_y), 10)
        pygame.draw.line(screen, (90, 50, 30), (self.origin_x, self.origin_y), (end_x, end_y), 12)

        # 3. Projétil e Vetores Vx (Azul) e Vy (Vermelho)
        if self.projectile_fired or len(self.path_points) > 0:
            cur_sx = self.origin_x + int(self.x * self.scale)
            cur_sy = self.origin_y - int(self.y * self.scale)
            pygame.draw.circle(screen, BLACK, (cur_sx, cur_sy), 6)

            # Cálculo e desenho dos vetores de velocidade instantânea
            rad = math.radians(self.angle)
            vx_inst = self.v0 * math.cos(rad)
            vy_inst = (self.v0 * math.sin(rad)) - (self.g * self.time)
            
            v_scale = 1.2
            vec_vx_len = int(vx_inst * v_scale)
            vec_vy_len = int(vy_inst * v_scale)

            # Vetor Vx (Horizontal - Azul)
            pygame.draw.line(screen, BLUE, (cur_sx, cur_sy), (cur_sx + vec_vx_len, cur_sy), 2)
            # Vetor Vy (Vertical - Vermelho)
            pygame.draw.line(screen, RED, (cur_sx, cur_sy), (cur_sx, cur_sy - vec_vy_len), 2)

        # 4. Painel Superior (Protegido contra IndexError)
        if self.lab_index < len(self.lab_questions):
            panel = pygame.Rect(50, 20, WIDTH - 100, 190)
            pygame.draw.rect(screen, (35, 40, 55), panel, border_radius=10)
            pygame.draw.rect(screen, WHITE, panel, 2, border_radius=10)

            q = self.lab_questions[self.lab_index]
            q_title = f"Laboratório de Lançamento - Questão {self.lab_index + 1}/{len(self.lab_questions)}"
            screen.blit(self.title_font.render(q_title, True, YELLOW), (70, 32))
            screen.blit(self.font.render(q["question"], True, WHITE), (70, 62))

            opt_y = 92
            for i, opt in enumerate(q["options"]):
                color = YELLOW if i == self.question_selected else WHITE
                prefix = "► " if i == self.question_selected else "   "
                screen.blit(self.font.render(prefix + opt, True, color), (70, opt_y))
                opt_y += 24

        # 5. Painel Inferior (Grandezas)
        dash = pygame.Rect(50, HEIGHT - 95, WIDTH - 100, 80)
        pygame.draw.rect(screen, (35, 40, 55), dash, border_radius=10)
        pygame.draw.rect(screen, WHITE, dash, 2, border_radius=10)

        info_text = f"v0: {self.v0:.1f} m/s | Ângulo: {self.angle:.1f}° | Tempo: {self.time:.1f}s | Altura: {max(0.0, self.y):.1f}m | Alcance: {self.x:.1f}m"
        screen.blit(self.bold_font.render(info_text, True, YELLOW), (70, HEIGHT - 85))
        
        controls_text = "Setas [←/→/↑/↓]: Ajustar Canhão | ESPAÇO: Disparar | W/S: Escolher Questão | ENTER: Confirmar"
        screen.blit(self.font.render(controls_text, True, WHITE), (70, HEIGHT - 55))