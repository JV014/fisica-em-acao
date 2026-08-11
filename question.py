import pygame
from settings import *

class Question:
    def __init__(self, difficulty="fundamental"):
        self.difficulty = difficulty
        self.phase = 1
        self.index = 0
        self.score = 0
        self.selected = 0

        # ==========================================
        # 9º ANO (FUNDAMENTAL) - Total de 15 questões
        # ==========================================
        self.fund_phase1 = [
            {"question": "O que caracteriza o Movimento Uniforme?", "options": ["A) A velocidade aumenta continuamente.", "B) A velocidade permanece constante.", "C) O corpo permanece em repouso.", "D) A distância permanece constante."], "correct": 1},
            {"question": "Um carro percorre 120 m em 4 s com velocidade constante. Qual a velocidade?", "options": ["A) 20 m/s", "B) 30 m/s", "C) 40 m/s", "D) 60 m/s"], "correct": 1},
            {"question": "No MU, a distância percorrida é proporcional a:", "options": ["A) Ao tempo gasto.", "B) À aceleração.", "C) À massa do veículo.", "D) Ao quadrado do tempo."], "correct": 0},
            {"question": "Se um móvel possui velocidade de 10 m/s, quanto percorre em 5 s?", "options": ["A) 2 m", "B) 15 m", "C) 50 m", "D) 100 m"], "correct": 2},
            {"question": "O gráfico da posição em função do tempo no MU é uma:", "options": ["A) Reta inclinada.", "B) Parábola.", "C) Linha horizontal.", "D) Hipérbole."], "correct": 0}
        ]

        self.fund_phase2 = [
            {"question": "No MUV, o que muda a cada segundo?", "options": ["A) A massa.", "B) A aceleração.", "C) A velocidade.", "D) A trajetória."], "correct": 2},
            {"question": "Um veículo parte do repouso e atinge 20 m/s em 4 s. Qual a aceleração?", "options": ["A) 2 m/s²", "B) 4 m/s²", "C) 5 m/s²", "D) 10 m/s²"], "correct": 2},
            {"question": "O que indica uma aceleração negativa (retardada)?", "options": ["A) O móvel está freiando/diminuindo a velocidade.", "B) O móvel está parado.", "C) O móvel está dando ré.", "D) A velocidade é constante."], "correct": 0},
            {"question": "No MUV, o gráfico da velocidade em função do tempo é uma:", "options": ["A) Reta inclinada.", "B) Parábola.", "C) Linha paralela ao eixo do tempo.", "D) Circunferência."], "correct": 0},
            {"question": "Um corpo em queda livre (sem resistência do ar) sofre a ação de qual força principal?", "options": ["A) A força magnética.", "B) A aceleração da gravidade.", "C) A força de atrito.", "D) A força centrífuga."], "correct": 1}
        ]

        self.fund_phase3 = [
            {"question": "Qual unidade do Sistema Internacional (SI) mede velocidade?", "options": ["A) km/h", "B) m/s", "C) cm/s", "D) mph"], "correct": 1},
            {"question": "Transformando 72 km/h para m/s, temos:", "options": ["A) 10 m/s", "B) 15 m/s", "C) 20 m/s", "D) 25 m/s"], "correct": 2},
            {"question": "Em física, o repouso ou o movimento de um corpo depende de:", "options": ["A) Do referencial adotado.", "B) Da temperatura.", "C) Da massa do objeto.", "D) Da cor do objeto."], "correct": 0},
            {"question": "Se um móvel tem aceleração constante de 3 m/s², sua velocidade a cada segundo aumenta em:", "options": ["A) 1 m/s", "B) 2 m/s", "C) 3 m/s", "D) 9 m/s"], "correct": 3},
            {"question": "Qual a fórmula básica da velocidade média no MU?", "options": ["A) V = S * t", "B) V = ΔS / Δt", "C) V = a * t²", "D) V = S0 + v*t"], "correct": 1}
        ]

        # ==========================================
        # ENSINO MÉDIO (AVANÇADO) - Total de 20 questões
        # ==========================================
        self.adv_phase1 = [
            {"question": "Um móvel desloca-se segundo S = 10 + 5t (SI). \n"
            "A posição inicial e a velocidade são:" , 
            "options": 
            ["A) S0=5m, v=10m/s", "B) S0=10m, v=5m/s", "C) S0=0m, v=15m/s", "D) S0=10m, v=15m/s"], "correct": 1},
            {"question": "Dada a função horária S = -5 + 12t,em qual \n"
             "instante o móvel passa pela origem?", "options": ["A) t = 0,4 s", "B) t = 1,2 s", "C) t = 2,4 s", "D) t = 5,0 s"], "correct": 1},
            {"question": "Dois móveis colidem na estrada quando possuem:", "options": ["A) A mesma velocidade.", "B) A mesma posição no mesmo instante.", "C) A mesma aceleração.", "D) Tempos de viagem iguais."], "correct": 1},
            {"question": "No MU, a área sob o gráfico da velocidade versus\n"
            " tempo representa:", "options": ["A) A aceleração.", "B) O deslocamento (ΔS).", "C) A posição final.", "D) O tempo total."], "correct": 1},
            {"question": "Um trem de 100 m atravessa um túnel de 400 m a 20 m/s.\n"
            "Qual o tempo total?", "options": ["A) 5 s", "B) 15 s", "C) 20 s", "D) 25 s"], "correct": 3}
        ]

        self.adv_phase2 = [
            {"question": "Um veículo a 72 km/h é freado até parar em 5 s.\n" 
             "Qual a aceleração escalar média?", "options": ["A) -2 m/s²", "B) -4 m/s²", "C) -14,4 m/s²", "D) -40 m/s²"], "correct": 1},
            {"question": "Dada a função horária do MUV S = 2 + 3t + t² (SI), \n"
             "qual a velocidade inicial?", "options": ["A) 2 m/s", "B) 3 m/s", "C) 1 m/s", "D) 4 m/s"], "correct": 1},
            {"question": "Qual a aceleração do móvel cuja função horária é S = 2 + 3t + t² (SI)?", "options": ["A) 1 m/s²", "B) 2 m/s²", "C) 3 m/s²", "D) 4 m/s²"], "correct": 1},
            {"question": "A Equação de Torricelli é muito útil quando o problema não fornece:", "options": ["A) A velocidade inicial.", "B) O tempo.", "C) A distância.", "D) A aceleração."], "correct": 1},
            {"question": "Um objeto em queda livre abandona o repouso de uma altura de 45 m. \n"
             "Qual o tempo?", "options": ["A) 2 s", "B) 3 s", "C) 4 s", "D) 5 s"], "correct": 1}
        ]

        self.adv_phase3 = [
            {"question": "Um móvel com aceleração constante tem sua velocidade \n"
             "triplicada em 4 s (5 para 20 m/s). Qual a aceleração?", "options": ["A) 2,5 m/s²", "B) 3,75 m/s²", "C) 5,0 m/s²", "D) 7,5 m/s²"], "correct": 1},
            {"question": "Se a velocidade de um corpo dobra no MUV partindo do\n"
            "repouso, a distância percorrida:", "options": ["A) Dobra", "B) Triplica", "C) Quadruplica", "D) Permanece igual"], "correct": 2},
            {"question": "O gráfico da posição em função do tempo para um MUV \n"
            "com aceleração positiva é uma:", "options": ["A) Reta crescente", "B) Reta decrescente", "C) Parábola com concavidade voltada para cima", "D) Parábola com concavidade voltada para baixo"], "correct": 2},
            {"question": "Em uma composição de movimentos (Galileu), o movimento \n"
            "na horizontal e na vertical são:", "options": ["A) Dependentes", "B) Independentes entre si", "C) Inversamente proporcionais", "D) Nulos"], "correct": 1},
            {"question": "Um ciclista pedala a 15 m/s e aplica os freios adquirindo\n"
              "desaceleração de -3 m/s². Qual a distância até parar?", "options": ["A) 25,0 m", "B) 37,5 m", "C) 50,0 m", "D) 75,0 m"], "correct": 1}
        ]

        self.oblique_questions = [
            {"question": "Qual ângulo de lançamento no vácuo proporciona \n"
             "o maior alcance horizontal?", "options": ["A) 30°", "B) 45°", "C) 60°", "D) 90°"], "correct": 1},
            {"question": "No ponto de altura máxima de um lançamento oblíquo, a componente\n "
            "vertical da velocidade é:", "options": ["A) Máxima", "B) Igual à horizontal", "C) Zero", "D) Constante"], "correct": 2},
            {"question": "O tempo de subida de um projétil lançado \n"
            "obliquamente é ______ o tempo de descida.", "options": ["A) Menor que", "B) Maior que", "C) Igual ao", "D) O dobro do"], "correct": 2},
            {"question": "Desprezando a resistência do ar, a componente horizontal\n"
            " da velocidade (Vx) no lançamento oblíquo:", "options": ["A) Aumenta", "B) Diminui", "C) Permanece constante", "D) É nula no ponto mais alto"], "correct": 2},
            {"question": "Se duplicarmos a velocidade inicial de lançamento de \n"
            "um projétil, o alcance máximo horizontal:", "options": ["A) Duplica", "B) Triplica", "C) Quadruplica", "D) Reduz à metade"], "correct": 2}
        ]

        self.title_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.option_font = pygame.font.SysFont("Arial", 18)

    def set_difficulty(self, diff):
        self.difficulty = diff

    def get_current_questions(self):
        if self.difficulty == "fundamental":
            if self.phase == 1: return self.fund_phase1
            elif self.phase == 2: return self.fund_phase2
            else: return self.fund_phase3
        else:
            if self.phase == 1: return self.adv_phase1
            elif self.phase == 2: return self.adv_phase2
            elif self.phase == 3: return self.adv_phase3
            else: return self.oblique_questions

    def check(self):
        current = self.get_current_questions()
        return self.selected == current[self.index]["correct"]

    def update_score(self, correct):
        if correct: self.score += 10

    def next_question(self):
        self.index += 1
        self.selected = 0

    def draw(self, screen):
        current = self.get_current_questions()
        if self.index >= len(current):
            return

        q = current[self.index]

        # Painel único unificado (amplo, cobrindo pergunta e alternativas)
        panel = pygame.Rect(120, 45, 760, 430)
        pygame.draw.rect(screen, (35, 35, 35), panel, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel, 3, border_radius=15)

        # Cabeçalho da fase/pontuação
        phase_str = f"Fase {self.phase} - Questão {self.index + 1}/{len(current)}   |   Pontos: {self.score}"
        p_title = self.title_font.render(phase_str, True, YELLOW)
        screen.blit(p_title, (160, 70))

        # Quebra automática de linha robusta (suporta \n manual e espaçamento automático)
        raw_lines = q["question"].split("\n")
        lines = []
        max_width = 680

        for raw_line in raw_lines:
            words = raw_line.strip().split(" ")
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.option_font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())

        # Renderiza as linhas da pergunta dentro do painel (usando option_font para o enunciado não ficar gigante)
        q_y = 105
        for line in lines:
            q_render = self.option_font.render(line, True, WHITE)
            screen.blit(q_render, (160, q_y))
            q_y += 24

        # Renderiza as alternativas dentro do painel unificado logo abaixo do enunciado
        y = q_y + 15
        for i, option in enumerate(q["options"]):
            color = YELLOW if i == self.selected else WHITE
            prefix = "x " if i == self.selected else "  "
            opt_render = self.option_font.render(prefix + option, True, color)
            screen.blit(opt_render, (160, y))
            y += 38