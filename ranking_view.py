import pygame
from settings import *

class RankingView:
    def __init__(self):
        self.tabs = [
            ("campaign", "Campanha"),
            ("multiplayer", "Multiplayer (Dupla)"),
            ("target", "Desafio Tiro ao Alvo"),
            ("players", "100 Primeiros Acessos")
        ]
        self.current_tab = 0
        self.scroll_offset = 0
        self.items_per_page = 10

        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.tab_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.row_font = pygame.font.SysFont("Arial", 18)
        self.counter_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 15)

    def reset(self):
        self.current_tab = 0
        self.scroll_offset = 0

    def handle_event(self, event, ranking_manager):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.current_tab = (self.current_tab + 1) % len(self.tabs)
                self.scroll_offset = 0
            elif event.key == pygame.K_LEFT:
                self.current_tab = (self.current_tab - 1) % len(self.tabs)
                self.scroll_offset = 0
            elif event.key == pygame.K_DOWN:
                total_items = self._get_current_list_len(ranking_manager)
                if self.scroll_offset + self.items_per_page < total_items:
                    self.scroll_offset += 1
            elif event.key == pygame.K_UP:
                if self.scroll_offset > 0:
                    self.scroll_offset -= 1
            elif event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                return True
        return False

    def _get_current_list_len(self, rm):
        key = self.tabs[self.current_tab][0]
        if key == "players":
            return len(rm.get_first_100_players())
        return len(rm.get_ranking(key))

    def draw(self, screen, ranking_manager):
        screen.fill((25, 30, 40))

        title = self.title_font.render("PAINEL DE RANKING E REGISTROS (TOP 100)", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        total_count = ranking_manager.get_total_players()
        badge_rect = pygame.Rect(WIDTH // 2 - 220, 62, 440, 36)
        pygame.draw.rect(screen, (40, 70, 50), badge_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 255, 150), badge_rect, 2, border_radius=8)
        count_txt = self.counter_font.render(f"Total de Jogadores Registrados: {total_count}", True, (100, 255, 150))
        screen.blit(count_txt, (WIDTH // 2 - count_txt.get_width() // 2, 68))

        tab_w = 215
        start_x = (WIDTH - (tab_w * len(self.tabs) + 30)) // 2
        for i, (_, label) in enumerate(self.tabs):
            rect = pygame.Rect(start_x + i * (tab_w + 10), 112, tab_w, 36)
            bg_color = YELLOW if i == self.current_tab else (45, 50, 65)
            txt_color = BLACK if i == self.current_tab else WHITE
            pygame.draw.rect(screen, bg_color, rect, border_radius=6)
            t_surf = self.tab_font.render(label, True, txt_color)
            screen.blit(t_surf, (rect.centerx - t_surf.get_width() // 2, rect.y + 8))

        table_rect = pygame.Rect(70, 160, WIDTH - 140, 370)
        pygame.draw.rect(screen, (35, 40, 52), table_rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, table_rect, 2, border_radius=12)

        key = self.tabs[self.current_tab][0]

        if key == "players":
            col1_x, col2_x, col3_x = 100, 220, 560
            screen.blit(self.tab_font.render("ORDEM", True, YELLOW), (col1_x, 175))
            screen.blit(self.tab_font.render("NOME DO JOGADOR", True, YELLOW), (col2_x, 175))
            screen.blit(self.tab_font.render("DATA / HORA DO ACESSO", True, YELLOW), (col3_x, 175))
            items = ranking_manager.get_first_100_players()
        else:
            col1_x, col2_x, col3_x, col4_x = 100, 190, 520, 690
            screen.blit(self.tab_font.render("POS.", True, YELLOW), (col1_x, 175))
            screen.blit(self.tab_font.render("JOGADOR", True, YELLOW), (col2_x, 175))
            screen.blit(self.tab_font.render("NÍVEL", True, YELLOW), (col3_x, 175))
            screen.blit(self.tab_font.render("PONTUAÇÃO", True, YELLOW), (col4_x, 175))
            items = ranking_manager.get_ranking(key)

        pygame.draw.line(screen, (100, 100, 120), (90, 202), (WIDTH - 90, 202), 1)

        if ranking_manager.is_syncing:
            loading = self.counter_font.render("Sincronizando dados em tempo real com a planilha...", True, YELLOW)
            screen.blit(loading, (WIDTH // 2 - loading.get_width() // 2, 310))
        elif not items:
            empty = self.row_font.render("Nenhum registro encontrado nesta categoria ainda.", True, (180, 180, 180))
            screen.blit(empty, (WIDTH // 2 - empty.get_width() // 2, 310))
        else:
            visible = items[self.scroll_offset : self.scroll_offset + self.items_per_page]
            y = 215
            for idx, item in enumerate(visible):
                real_pos = self.scroll_offset + idx + 1

                if key == "players":
                    color = (230, 235, 245)
                    screen.blit(self.row_font.render(f"#{item['order']}", True, (150, 200, 255)), (col1_x, y))
                    screen.blit(self.row_font.render(item['name'], True, color), (col2_x, y))
                    screen.blit(self.row_font.render(item['timestamp'], True, color), (col3_x, y))
                else:
                    if real_pos == 1:
                        color = YELLOW
                    elif real_pos == 2:
                        color = (210, 210, 210)
                    elif real_pos == 3:
                        color = (205, 127, 50)
                    else:
                        color = WHITE

                    diff_label = "Fundamental" if item["difficulty"] == "fundamental" else ("Ensino Médio" if item["difficulty"] == "medio" else "-")
                    screen.blit(self.row_font.render(f"{real_pos}º", True, color), (col1_x, y))
                    screen.blit(self.row_font.render(item['name'], True, color), (col2_x, y))
                    screen.blit(self.row_font.render(diff_label, True, color), (col3_x, y))
                    screen.blit(self.row_font.render(f"{item['score']} pts", True, color), (col4_x, y))

                y += 30

        footer = self.info_font.render("Use [← / →] para trocar de ranking | [↑ / ↓] para rolar até o 100º | [ENTER / ESC] Voltar", True, WHITE)
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, 548))