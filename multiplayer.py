import pygame
from settings import *

class Multiplayer:
    def __init__(self, difficulty="fundamental"):
        self.difficulty = difficulty
        self.index = 0
        self.score_p1 = 0
        self.score_p2 = 0
        self.selected_p1 = 0
        self.selected_p2 = 0
        self.p1_submitted = False
        self.p2_submitted = False
        self.show_feedback = False

        try:
            self.car_img = pygame.image.load("assets/images/car.png")
            self.car_img = pygame.transform.scale(self.car_img, (110, 55))
        except Exception:
            self.car_img = None

        self.car_x = -130
        self.car_speed = 140

        from question import Question
        q_ref = Question(self.difficulty)
        
        if self.difficulty == "fundamental":
            self.all_questions = q_ref.fund_phase1 + q_ref.fund_phase2 + q_ref.fund_phase3
        else:
            self.all_questions = q_ref.adv_phase1 + q_ref.adv_phase2 + q_ref.adv_phase3 + q_ref.oblique_questions

        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.question_font = pygame.font.SysFont("Arial", 18)
        self.option_font = pygame.font.SysFont("Arial", 16)
        self.info_font = pygame.font.SysFont("Arial", 16, bold=True)
        self.success_font = pygame.font.SysFont("Arial", 36, bold=True)

    def set_difficulty(self, diff):
        self.difficulty = diff
        from question import Question
        q_ref = Question(self.difficulty)
        if self.difficulty == "fundamental":
            self.all_questions = q_ref.fund_phase1 + q_ref.fund_phase2 + q_ref.fund_phase3
        else:
            self.all_questions = q_ref.adv_phase1 + q_ref.adv_phase2 + q_ref.adv_phase3 + q_ref.oblique_questions

    def reset(self):
        self.index = 0
        self.score_p1 = 0
        self.score_p2 = 0
        self.selected_p1 = 0
        self.selected_p2 = 0
        self.p1_submitted = False
        self.p2_submitted = False
        self.show_feedback = False
        self.car_x = -130

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.finished():
                current_q = self.all_questions[self.index]
                total_opts = len(current_q["options"])

                if not self.show_feedback:
                    # Jogador 1: W / S e ENTER
                    if not self.p1_submitted:
                        if event.key == pygame.K_s: 
                            self.selected_p1 = (self.selected_p1 + 1) % total_opts
                        elif event.key == pygame.K_w: 
                            self.selected_p1 = (self.selected_p1 - 1) % total_opts
                        elif event.key == pygame.K_RETURN: 
                            self.p1_submitted = True

                    # Jogador 2: Setas para cima / baixo e ESPAÇO
                    if not self.p2_submitted:
                        if event.key == pygame.K_DOWN: 
                            self.selected_p2 = (self.selected_p2 + 1) % total_opts
                        elif event.key == pygame.K_UP: 
                            self.selected_p2 = (self.selected_p2 - 1) % total_opts
                        elif event.key == pygame.K_SPACE: 
                            self.p2_submitted = True

                    if self.p1_submitted and self.p2_submitted:
                        if self.selected_p1 == current_q["correct"]: self.score_p1 += 10
                        if self.selected_p2 == current_q["correct"]: self.score_p2 += 10
                        self.show_feedback = True
                else:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        self.index += 1
                        self.selected_p1 = 0
                        self.selected_p2 = 0
                        self.p1_submitted = False
                        self.p2_submitted = False
                        self.show_feedback = False

    def finished(self):
        return self.index >= len(self.all_questions)

    def update(self, dt):
        if not self.finished():
            self.car_x += self.car_speed * dt
            if self.car_x > WIDTH: self.car_x = -130

    def draw(self, screen):
        screen.fill((20, 20, 25))
        
        if not self.finished():
            q = self.all_questions[self.index]
            half_w = WIDTH // 2

            # P1
            p1_bg = pygame.Rect(10, 10, half_w - 15, HEIGHT - 65)
            pygame.draw.rect(screen, (25, 40, 60), p1_bg, border_radius=12)
            pygame.draw.rect(screen, (100, 200, 255), p1_bg, 2, border_radius=12)
            screen.blit(self.title_font.render("JOGADOR 1", True, (100, 200, 255)), (30, 25))
            screen.blit(self.info_font.render(f"Pontos: {self.score_p1}", True, WHITE), (30, 60))
            screen.blit(self.question_font.render(q["question"], True, WHITE), (30, 100))

            y = 160
            for i, opt in enumerate(q["options"]):
                color = (255, 255, 100) if i == self.selected_p1 else WHITE
                screen.blit(self.option_font.render(("x " if i == self.selected_p1 else "   ") + opt, True, color), (30, y))
                y = y + 45
            screen.blit(self.info_font.render("PRONTO!" if self.p1_submitted else "Escolhendo (W/S + ENTER)...", True, (100, 255, 100) if self.p1_submitted else (200, 200, 200)), (30, HEIGHT - 95))

            # P2
            p2_bg = pygame.Rect(half_w + 5, 10, half_w - 15, HEIGHT - 65)
            pygame.draw.rect(screen, (60, 50, 25), p2_bg, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 100), p2_bg, 2, border_radius=12)
            screen.blit(self.title_font.render("JOGADOR 2", True, (255, 255, 100)), (half_w + 25, 25))
            screen.blit(self.info_font.render(f"Pontos: {self.score_p2}", True, WHITE), (half_w + 25, 60))
            screen.blit(self.question_font.render(q["question"], True, WHITE), (half_w + 25, 100))

            y = 160
            for i, opt in enumerate(q["options"]):
                color = (255, 255, 100) if i == self.selected_p2 else WHITE
                screen.blit(self.option_font.render(("x " if i == self.selected_p2 else "   ") + opt, True, color), (half_w + 25, y))
                y = y + 45
            screen.blit(self.info_font.render("PRONTO!" if self.p2_submitted else "Escolhendo ([↑ / ↓] + ESPAÇO)...", True, (100, 255, 100) if self.p2_submitted else (200, 200, 200)), (half_w + 25, HEIGHT - 95))

            pygame.draw.line(screen, YELLOW, (half_w, 10), (half_w, HEIGHT - 65), 3)
            badge_rect = pygame.Rect(half_w - 55, 15, 110, 30)
            pygame.draw.rect(screen, (30, 30, 35), badge_rect, border_radius=8)
            pygame.draw.rect(screen, YELLOW, badge_rect, 2, border_radius=8)
            screen.blit(self.info_font.render(f"Q: {self.index + 1}/{len(self.all_questions)}", True, YELLOW), (half_w - 35, 20))

            # Pista inferior
            track_y = HEIGHT - 55
            pygame.draw.rect(screen, (50, 50, 55), (0, track_y, WIDTH, 55))
            pygame.draw.line(screen, WHITE, (0, track_y), (WIDTH, track_y), 2)
            offset = int(self.car_x * 1.5) % 40
            for dash_x in range(-40, WIDTH + 40, 40):
                pygame.draw.rect(screen, YELLOW, (dash_x - offset, track_y + 25, 20, 4))
            if self.car_img: screen.blit(self.car_img, (int(self.car_x), track_y + 5))

            if self.show_feedback:
                fb_rect = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 50, 500, 100)
                pygame.draw.rect(screen, (20, 100, 20), fb_rect, border_radius=12)
                pygame.draw.rect(screen, WHITE, fb_rect, 2, border_radius=12)
                screen.blit(self.title_font.render(f"Gabarito: Alternativa {chr(65 + q['correct'])}", True, YELLOW), (WIDTH // 2 - 130, HEIGHT // 2 - 35))
                screen.blit(self.info_font.render("Pressione [ENTER] ou [ESPAÇO] para continuar", True, WHITE), (WIDTH // 2 - 170, HEIGHT // 2 + 10))
        else:
            # TELA FINAL DO MULTIPLAYER (FORÇADA E GARANTIDA)
            end_rect = pygame.Rect(WIDTH // 2 - 320, HEIGHT // 2 - 180, 640, 360)
            pygame.draw.rect(screen, (35, 40, 55), end_rect, border_radius=15)
            pygame.draw.rect(screen, YELLOW, end_rect, 3, border_radius=15)
            
            title_text = self.success_font.render("FIM DA PARTIDA MULTIPLAYER!", True, YELLOW)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, end_rect.y + 25))
            
            if self.score_p1 > self.score_p2:
                msg = "VENCEDOR: JOGADOR 1!"
            elif self.score_p2 > self.score_p1:
                msg = "VENCEDOR: JOGADOR 2!"
            else:
                msg = "EMPATE TÉCNICO!"
                
            winner_text = self.title_font.render(msg, True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, end_rect.y + 90))
            
            p1_text = self.title_font.render(f"Placar Jogador 1: {self.score_p1} pts", True, (100, 200, 255))
            p2_text = self.title_font.render(f"Placar Jogador 2: {self.score_p2} pts", True, (255, 255, 100))
            
            screen.blit(p1_text, (WIDTH // 2 - p1_text.get_width() // 2, end_rect.y + 150))
            screen.blit(p2_text, (WIDTH // 2 - p2_text.get_width() // 2, end_rect.y + 195))
            
            footer_text = self.info_font.render("Pressione [ENTER] ou [ESC] para voltar ao Menu", True, YELLOW)
            screen.blit(footer_text, (WIDTH // 2 - footer_text.get_width() // 2, end_rect.y + 280))