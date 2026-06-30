import pygame
from settings import *

class Question:

    def __init__(self):

        # Questão atual
        self.index = 0

        # Alternativa selecionada
        self.selected = 0

        # Pontuação
        self.score = 0

        # Banco de questões

        self.phase = 1
        self.easy_questions = [

            {
                "question": "O que caracteriza o Movimento Uniforme?",

                "options": [
                    "A) A velocidade aumenta continuamente.",
                    "B) A velocidade permanece constante.",
                    "C) O corpo permanece em repouso.",
                    "D) A distância permanece constante."
                ],

                "correct": 1
            },

            {
                "question": "No Movimento Uniforme, a aceleração é:",

                "options": [
                    "A) Positiva.",
                    "B) Negativa.",
                    "C) Igual a zero.",
                    "D) Variável."
                ],

                "correct": 2
            },

            {
                "question": "Um carro percorre 120 m com velocidade constante de 20 m/s. O tempo gasto é:",

                "options": [
                    "A) 4 s",
                    "B) 5 s",
                    "C) 6 s",
                    "D) 8 s"
                ],

                "correct": 2
            },

            {
                "question": "Um carro percorreu 300 m em 15 s. Sua velocidade é:",

                "options": [
                    "A) 15 m/s",
                    "B) 20 m/s",
                    "C) 25 m/s",
                    "D) 30 m/s"
                ],

                "correct": 1
            },

            {
                "question": "Um carro move-se a 15 m/s durante 12 s. Qual a distância percorrida?",

                "options": [
                    "A) 150 m",
                    "B) 160 m",
                    "C) 170 m",
                    "D) 180 m"
                ],

                "correct": 3
            }


        ]

        self.medium_questions = [

    {
        "question": "O que é aceleração?",

        "options": [
            "A) A distância percorrida.",
            "B) A variação da velocidade em relação ao tempo.",
            "C) A posição do corpo.",
            "D) O deslocamento."
        ],

        "correct": 1
    },

    {
        "question": "A unidade da aceleração no SI é:",

        "options": [
            "A) m",
            "B) m/s",
            "C) m/s²",
            "D) km/h"
        ],

        "correct": 2
    },

    {
        "question": "Quando um veículo aumenta sua velocidade, sua aceleração é:",

        "options": [
            "A) Nula.",
            "B) Positiva.",
            "C) Negativa.",
            "D) Constante e negativa."
        ],

        "correct": 1
    },

    {
        "question":"Um carro passa de 10 m/s para 20 m/s em 5 s. Qual é sua aceleração?",

        "options": [
            "A) 1 m/s²",
            "B) 2 m/s²",
            "C) 3 m/s²",
            "D) 4 m/s²"
        ],

        "correct": 1
    },

    {
        "question": "A expressão da aceleração média é:",

        "options": [
            "A) v = ΔS/Δt",
            "B) a = Δv/Δt",
            "C) S = S₀ + vt",
            "D) F = ma"
        ],

        "correct": 1
    }

   ]
        self.hard_questions = [

            {
    "question": "Um carro parte do repouso e acelera a 2 m/s² durante 8 s. Qual será sua velocidade final?",

    "options": [

        "A) 12 m/s",
        "B) 14 m/s",
        "C) 16 m/s",
        "D) 18 m/s"

    ],

    "correct": 2
},
    {
    "question": "Um carro parte do repouso com aceleração constante de 2 m/s². Qual distância percorre em 6 s?",

    "options": [

        "A) 24 m",
        "B) 30 m",
        "C) 36 m",
        "D) 48 m"

    ],

    "correct": 2
},   
     {
    "question": "Um automóvel possui velocidade inicial de 5 m/s e aceleração de 3 m/s² durante 5 s. Qual será sua velocidade final?",

    "options": [

        "A) 15 m/s",
        "B) 18 m/s",
        "C) 20 m/s",
        "D) 22 m/s"

    ],

    "correct": 2
},   

    {
    "question": "Um veículo parte da posição 20 m, com velocidade inicial de 4 m/s e aceleração de 2 m/s² durante 6 s. Qual será sua posição final?",

    "options": [

        "A) 56 m",
        "B) 68 m",
        "C) 80 m",
        "D) 92 m"

    ],

    "correct": 2
},
     {
    "question": "Um carro aumenta sua velocidade de 10 m/s para 30 m/s percorrendo 200 m. Qual foi sua aceleração?",

    "options": [

        "A) 1,5 m/s²",
        "B) 2,0 m/s²",
        "C) 2,5 m/s²",
        "D) 3,0 m/s²"

    ],

    "correct": 1
}
        ]
       
        # Fontes
        self.title_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.question_font = pygame.font.SysFont("Arial", 30)
        self.option_font = pygame.font.SysFont("Arial", 28)
        self.info_font = pygame.font.SysFont("Arial", 22)

# ==========================================
# ESCREVER TEXTO COM QUEBRA DE LINHA
# ==========================================

    def draw_text(self, screen, text, x, y, max_width):
        
        words = text.split()

        line = ""

        for word in words:
            test_line = line + word + " "

            if self.question_font.size(test_line)[0] <= max_width:
                line = test_line

            else:
                render = self.question_font.render(
                    line,
                    True,
                    WHITE
                )

                screen.blit(render, (x, y))

                y += 40

                line = word + " "

        if line != "":
            render = self.question_font.render(
                line,
                True,
                WHITE)
            screen.blit(render, (x, y))
    
    # ==========================================
    # DESENHAR QUESTÃO
    # ==========================================

    def get_current_questions(self):
            if self.phase == 1:
                return self.easy_questions
            elif self.phase == 2:
                return self.medium_questions
            else:
                return self.hard_questions
            

    

    def draw(self, screen):
        
        q = self.get_current_questions()[self.index]

        painel = pygame.Rect(80, 50, 840, 500)

        pygame.draw.rect(
            screen,
            (35, 35, 35),
            painel,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            WHITE,
            painel,
            3,
            border_radius=15
        )

        titulo = self.title_font.render(
            f"QUESTÃO {self.index + 1}",
            True,
            YELLOW
        )

        screen.blit(titulo, (300, 80))

        self.draw_text(screen, q["question"], 120, 160, 720)
        

        y = 240

        for i, alternativa in enumerate(q["options"]):

            if i == self.selected:

                texto = "► " + alternativa
                cor = YELLOW

            else:

                texto = "   " + alternativa
                cor = WHITE

            render = self.option_font.render(
                texto,
                True,
                cor
            )

            screen.blit(render, (140, y))

            y += 55

        pontos = self.info_font.render(
            f"Pontuação: {self.score}/150",
            True,
            WHITE
        )

        screen.blit(pontos, (650, 510))

    # ==========================================
    # VERIFICAR RESPOSTA
    # ==========================================

    def check(self):

        
        q = self.get_current_questions()[self.index]

        return self.selected == q["correct"]

    # ==========================================
    # ADICIONAR PONTOS
    # ==========================================

    def add_score(self):

        self.score += 10
    
    #=========================================
    # PERDER PONTOS
    #=========================================
    def remove_score(self):
        
        self.score -= 5

        if self.score < 0: 
            self.score = 0

    # ==========================================
    # PRÓXIMA QUESTÃO
    # ==========================================

    def next_question(self):

        self.index += 1
        self.selected = 0

    # ==========================================
    # QUESTÕES FINALIZADAS?
    # ==========================================

    def finished(self):

        return self.index >= len(self.get_current_questions())

    # ==========================================
    # ALTERNATIVA CORRETA
    # ==========================================

    def correct_option(self):

        return self.get_current_questions()[self.index]["correct"]