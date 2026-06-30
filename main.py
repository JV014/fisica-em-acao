import pygame
import sys

from settings import *
from player import Car
from road import Road
from menu import Menu
from intro import Intro
from question import Question
from feedback import Feedback
from simulation import Simulation
from result import Result
from phase import Phase
from credits import Credits


# ======================================
# ESTADOS DO JOGO
# ======================================

MENU = 0
INTRO = 1
QUESTION = 2
FEEDBACK = 3
SIMULATION = 4
PHASE = 5
RESULT = 6
CREDITS = 7
# ======================================
# INICIALIZAÇÃO
# ======================================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

# ======================================
# CARREGAR IMAGEM
# ======================================

car_image = pygame.image.load(
    "assets/images/car.png"
).convert_alpha()

car_image = pygame.transform.scale(
    car_image,
    (170, 85)
)

# ======================================
# OBJETOS
# ======================================

road = Road()

car = Car(
    50,
    335,
    car_image
)

car.vx = 60

menu = Menu()

intro = Intro()

question = Question()

feedback = Feedback()

simulation = Simulation()

result = Result()

phase = Phase()

credits = Credits()

game_state = MENU

running = True

# ======================================
# LOOP PRINCIPAL
# ======================================

while running:

    dt = clock.tick(FPS)/1000

    # ===============================
    # EVENTOS
    # ===============================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ---------------- MENU ----------------

        if game_state == MENU:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:

                    menu.selected += 1

                    if menu.selected >= len(menu.options):
                        menu.selected = 0

                elif event.key == pygame.K_UP:

                    menu.selected -= 1

                    if menu.selected < 0:
                        menu.selected = len(menu.options)-1

                elif event.key == pygame.K_RETURN:

                    if menu.selected == 0:
                        game_state = INTRO

                    elif menu.selected == 1:
                        game_state = CREDITS

                    elif menu.selected == 2:
                        running = False

        # ---------------- INTRO ----------------

        elif game_state == INTRO:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    game_state = QUESTION

        # ---------------- QUESTÕES ----------------

        elif game_state == QUESTION:
            current = question.get_current_questions()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:

                    question.selected += 1

                    current = question.get_current_questions()
                if question.selected >= len(current[question.index]["options"]):
                    question.selected = 0

                elif event.key == pygame.K_UP:

                    question.selected -= 1

                    current = question.get_current_questions()
                if question.selected < 0:
                    question.selected = len(current[question.index]["options"])-1

                elif event.key == pygame.K_RETURN:
                    if question.check():
                        feedback.set_feedback(True)
                    else:
                        feedback.set_feedback(False)
                    game_state = FEEDBACK
        elif game_state == FEEDBACK:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if feedback.correct:
                        question.add_score()
                        question.next_question()
                        #mudar de cenario conforme a dificuldade da questão
                        if question.phase == 1 and question.index ==5: 
                            question.phase = 2
                            question.index = 0

                            road.level = "medium"

                            phase.set_phase(2)
                            game_state = PHASE

                        elif question.phase == 2 and question.index ==5:
                            question.phase = 3
                            question.index = 0

                            road.level = "hard"

                            phase.set_phase(3)
                            game_state = PHASE     

                        if question.finished():
                            game_state = RESULT
                            
                        else: 
                            simulation.start(car)
                            game_state = SIMULATION
                    else:
                        question.remove_score()
                        game_state = QUESTION
    
        elif game_state == PHASE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    simulation.start(car)
                    game_state = SIMULATION
        elif game_state == CREDITS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = MENU

        # ---------------- SIMULAÇÃO ----------------
    if game_state == SIMULATION:
        simulation.update(car, dt)
        if simulation.finished():
            game_state = QUESTION
    # =====================================
    # DESENHO
    # =====================================

    if game_state == MENU:

        menu.draw(screen)

    elif game_state == INTRO:

        road.draw(screen)

        car.draw(screen)

        intro.draw(screen)

    elif game_state == QUESTION:


        road.draw(screen)

        car.draw(screen)

        question.draw(screen)
    
    elif game_state == PHASE:

        phase.draw(screen)
        road.draw(screen)
        car.draw(screen)
    
    elif game_state == FEEDBACK:

        road.draw(screen)

        car.draw(screen)

        feedback.draw(screen)
    elif game_state == CREDITS:

        credits.draw(screen)
    elif game_state == SIMULATION:
        
        
        road.draw(screen)

        car.draw(screen)

    elif game_state == RESULT:

        result.draw(screen, question.score)
    pygame.display.flip()

pygame.quit()

sys.exit()