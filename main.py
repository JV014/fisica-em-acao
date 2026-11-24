import asyncio
import pygame
import sys

from settings import *
from player import Car
from road import Road
from menu import Menu
from intro import Intro
from level_selection import LevelSelection
from multiplayer_intro import MultiplayerIntro
from exploration_intro import ExplorationIntro
from target_intro import TargetIntro
from question import Question
from feedback import Feedback
from simulation import Simulation
from exploration_mode import ExplorationMode
from free_laboratory import FreeLaboratory
from target_challenge import TargetChallenge
from result import Result
from phase import Phase
from credits import Credits
from multiplayer import Multiplayer

from ranking_manager import RankingManager
from player_register import PlayerRegister
from ranking_view import RankingView

MENU = 0
LEVEL_SELECT = 15
INTRO = 1
QUESTION = 2
FEEDBACK = 3
SIMULATION = 4
FREE_LAB = 5
EXPLORATION = 10
PHASE = 6
TARGET_CHALLENGE = 7
RESULT = 8
CREDITS = 9
MULTIPLAYER = 11
MULTIPLAYER_INTRO = 12
EXPLORATION_INTRO = 13
TARGET_INTRO = 14
REGISTER_PLAYER = 16
REGISTER_P2 = 17
RANKING = 18

async def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        pass

    is_muted = False
    try:
        pygame.mixer.music.load("assets/sounds/shavonne (2).mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
    except Exception as e:
        print(f"Aviso: Não foi possível carregar a música de fundo: {e}")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    car_image = pygame.image.load("assets/images/car.png")
    car_image = pygame.transform.scale(car_image, (170, 85))

    road = Road()
    car = Car(50, 335, car_image)
    car.vx = 60

    menu = Menu()
    level_selection = LevelSelection()
    intro = Intro()
    multiplayer_intro = MultiplayerIntro()
    exploration_intro = ExplorationIntro()
    target_intro = TargetIntro()

    question = Question()
    feedback = Feedback()
    simulation = Simulation()
    exploration = ExplorationMode()
    free_lab = FreeLaboratory()
    target_challenge = TargetChallenge()
    result = Result()
    phase = Phase()
    credits = Credits()
    multiplayer = Multiplayer()

    ranking_manager = RankingManager()
    player_register = PlayerRegister()
    ranking_view = RankingView()

    game_state = REGISTER_PLAYER
    selected_mode = None
    current_difficulty = "fundamental"
    current_player_name = ""
    campaign_saved = False

    running = True

    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and game_state not in [REGISTER_PLAYER, REGISTER_P2]:
                    is_muted = not is_muted
                    if is_muted:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                if event.key == pygame.K_ESCAPE:
                    if game_state in [FREE_LAB, EXPLORATION, TARGET_CHALLENGE, SIMULATION, MULTIPLAYER, MULTIPLAYER_INTRO, EXPLORATION_INTRO, TARGET_INTRO, LEVEL_SELECT, RANKING]:
                        game_state = MENU

            # ---------------- CADASTRO INICIAL DO JOGADOR ----------------
            if game_state == REGISTER_PLAYER:
                entered_name = player_register.handle_event(event)
                if entered_name:
                    current_player_name = entered_name
                    game_state = MENU
                    asyncio.create_task(ranking_manager.register_player_access(entered_name))

            # ---------------- CADASTRO DO JOGADOR 2 (MULTIPLAYER) ----------------
            elif game_state == REGISTER_P2:
                entered_p2 = player_register.handle_event(event)
                if entered_p2:
                    multiplayer.p1_name = current_player_name
                    multiplayer.p2_name = entered_p2
                    game_state = MULTIPLAYER_INTRO
                    asyncio.create_task(ranking_manager.register_player_access(entered_p2))

            # ---------------- PAINEL DE RANKING E REGISTROS ----------------
            elif game_state == RANKING:
                if ranking_view.handle_event(event, ranking_manager):
                    game_state = MENU

            # ---------------- MENU ----------------
            elif game_state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu.selected = (menu.selected + 1) % len(menu.options)
                    elif event.key == pygame.K_UP:
                        menu.selected = (menu.selected - 1) % len(menu.options)
                    elif event.key == pygame.K_RETURN:
                        if menu.selected == 0:  # Jogar Campanha
                            selected_mode = "campaign"
                            campaign_saved = False
                            game_state = LEVEL_SELECT
                        elif menu.selected == 1:  # Jogar Campanha Multiplayer
                            selected_mode = "multiplayer"
                            game_state = LEVEL_SELECT
                        elif menu.selected == 2:  # Laboratório de Lançamento
                            game_state = EXPLORATION_INTRO
                        elif menu.selected == 3:  # Desafio Tiro ao Alvo
                            game_state = TARGET_INTRO
                        elif menu.selected == 4:  # Ranking e Registros
                            ranking_view.reset()
                            game_state = RANKING
                            asyncio.create_task(ranking_manager.sync_from_cloud())
                        elif menu.selected == 5:  # Créditos
                            game_state = CREDITS
                        elif menu.selected == 6:  # Sair
                            running = False

            # ---------------- SELEÇÃO DE NÍVEL ----------------
            elif game_state == LEVEL_SELECT:
                res = level_selection.handle_event(event)
                if res:
                    current_difficulty = res
                    if selected_mode == "campaign":
                        question.set_difficulty(current_difficulty)
                        question.phase = 1
                        question.index = 0
                        question.score = 0
                        exploration.reset()
                        road.level = "easy"
                        game_state = INTRO
                    elif selected_mode == "multiplayer":
                        multiplayer.set_difficulty(current_difficulty)
                        multiplayer.reset()
                        player_register.reset()
                        game_state = REGISTER_P2

            # ---------------- INTRO CAMPANHA ----------------
            elif game_state == INTRO:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = QUESTION

            # ---------------- INTRO MULTIPLAYER ----------------
            elif game_state == MULTIPLAYER_INTRO:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = MULTIPLAYER

            # ---------------- INTRO EXPLORAÇÃO / LAB LIVRE ----------------
            elif game_state == EXPLORATION_INTRO:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    free_lab.reset_projectile()
                    game_state = FREE_LAB

            # ---------------- INTRO TIRO AO ALVO ----------------
            elif game_state == TARGET_INTRO:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    target_challenge.set_mode(is_campaign=False)
                    game_state = TARGET_CHALLENGE

            # ---------------- QUESTÕES (Fases da Campanha) ----------------
            elif game_state == QUESTION:
                current = question.get_current_questions()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        question.selected = (question.selected + 1) % len(current[question.index]["options"])
                    elif event.key == pygame.K_UP:
                        question.selected = (question.selected - 1) % len(current[question.index]["options"])
                    elif event.key == pygame.K_RETURN:
                        feedback.set_feedback(question.check())
                        game_state = FEEDBACK

            # ---------------- FEEDBACK DA RESPOSTA ----------------
            elif game_state == FEEDBACK:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if current_difficulty == "fundamental" or question.phase < 4:
                        question.update_score(feedback.correct)
                    
                    question.next_question()
                    current_list = question.get_current_questions()

                    if question.index >= len(current_list):
                        if current_difficulty == "fundamental":
                            if question.phase >= 3:
                                game_state = RESULT
                            else:
                                question.phase += 1
                                question.index = 0
                                road.level = "medium" if question.phase == 2 else "hard"
                                phase.set_phase(question.phase)
                                game_state = PHASE
                        else:
                            if question.phase == 1:
                                question.phase = 2
                                question.index = 0
                                road.level = "medium"
                                phase.set_phase(2)
                                game_state = PHASE
                            elif question.phase == 2:
                                question.phase = 3
                                question.index = 0
                                road.level = "hard"
                                phase.set_phase(3)
                                game_state = PHASE
                            elif question.phase == 3:
                                question.phase = 4
                                question.index = 0
                                phase.set_phase(4)
                                game_state = PHASE
                            elif question.phase == 4:
                                target_challenge.set_mode(is_campaign=True)
                                game_state = TARGET_CHALLENGE
                    else:
                        if question.phase == 4 and current_difficulty == "medio":
                            if exploration.finished():
                                target_challenge.set_mode(is_campaign=True)
                                game_state = TARGET_CHALLENGE
                            else:
                                game_state = EXPLORATION
                        else:
                            simulation.start(car)
                            game_state = SIMULATION
        
            # ---------------- APRESENTAÇÃO DE FASE ----------------
            elif game_state == PHASE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if question.phase == 4 and current_difficulty == "medio":
                        exploration.reset_projectile()
                        game_state = EXPLORATION
                    else:
                        simulation.start(car)
                        game_state = SIMULATION

            # ---------------- EXPLORAÇÃO (Campanha Fase 4) ----------------
            elif game_state == EXPLORATION:
                answered = exploration.handle_event(event, question, feedback)
                if answered:
                    game_state = FEEDBACK

            # ---------------- LABORATÓRIO LIVRE (Menu) ----------------
            elif game_state == FREE_LAB:
                free_lab.handle_event(event)

            # ---------------- 2 PLAYERS ----------------
            elif game_state == MULTIPLAYER:
                if multiplayer.finished():
                    if not multiplayer.score_saved:
                        multiplayer.score_saved = True
                        asyncio.create_task(ranking_manager.add_score("multiplayer", multiplayer.p1_name, multiplayer.score_p1, current_difficulty))
                        asyncio.create_task(ranking_manager.add_score("multiplayer", multiplayer.p2_name, multiplayer.score_p2, current_difficulty))
                    if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        game_state = MENU
                else:
                    multiplayer.handle_event(event)

            # ---------------- TIRO AO ALVO ----------------
            elif game_state == TARGET_CHALLENGE:
                target_challenge.handle_event(event)
                if target_challenge.all_completed and not target_challenge.campaign_mode and not target_challenge.score_saved:
                    target_challenge.score_saved = True
                    asyncio.create_task(ranking_manager.add_score("target", current_player_name, target_challenge.score))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if target_challenge.campaign_mode and (target_challenge.hit or target_challenge.attempts_left <= 0):
                        if target_challenge.hit and not target_challenge.score_added:
                            question.score += 100
                            target_challenge.score_added = True
                        game_state = RESULT
                    elif target_challenge.all_completed and not target_challenge.campaign_mode:
                        game_state = MENU

            # ---------------- RESULTADO FINAL DA CAMPANHA ----------------
            elif game_state == RESULT:
                if not campaign_saved:
                    campaign_saved = True
                    asyncio.create_task(ranking_manager.add_score("campaign", current_player_name, question.score, current_difficulty))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = MENU
            
            # ---------------- CRÉDITOS ----------------
            elif game_state == CREDITS:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = MENU

        # ===============================
        # ATUALIZAÇÕES CONTÍNUAS (DT)
        # ===============================
        if game_state == SIMULATION:
            simulation.update(car, dt)
            if simulation.finished():
                game_state = QUESTION
        elif game_state == EXPLORATION:
            exploration.update(dt)
        elif game_state == FREE_LAB:
            free_lab.update(dt)
        elif game_state == MULTIPLAYER:
            multiplayer.update(dt)
            if multiplayer.finished() and not multiplayer.score_saved:
                multiplayer.score_saved = True
                asyncio.create_task(ranking_manager.add_score("multiplayer", multiplayer.p1_name, multiplayer.score_p1, current_difficulty))
                asyncio.create_task(ranking_manager.add_score("multiplayer", multiplayer.p2_name, multiplayer.score_p2, current_difficulty))
        elif game_state == TARGET_CHALLENGE:
            target_challenge.update(dt)
            if target_challenge.all_completed and not target_challenge.campaign_mode and not target_challenge.score_saved:
                target_challenge.score_saved = True
                asyncio.create_task(ranking_manager.add_score("target", current_player_name, target_challenge.score))

        # =====================================
        # DESENHO NA TELA
        # =====================================
        if game_state == REGISTER_PLAYER:
            player_register.draw(screen)
        elif game_state == REGISTER_P2:
            player_register.draw(screen, "MODO MULTIPLAYER (DUPLA)", "Digite o nome do JOGADOR 2:")
        elif game_state == MENU:
            menu.draw(screen, current_player_name)
        elif game_state == RANKING:
            ranking_view.draw(screen, ranking_manager)
        elif game_state == LEVEL_SELECT:
            road.draw(screen)
            car.draw(screen)
            level_selection.draw(screen)
        elif game_state == INTRO:
            road.draw(screen)
            car.draw(screen)
            intro.draw(screen)
        elif game_state == MULTIPLAYER_INTRO:
            road.draw(screen)
            car.draw(screen)
            multiplayer_intro.draw(screen)
        elif game_state == EXPLORATION_INTRO:
            road.draw(screen)
            car.draw(screen)
            exploration_intro.draw(screen)
        elif game_state == TARGET_INTRO:
            road.draw(screen)
            car.draw(screen)
            target_intro.draw(screen)
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
            road.draw(screen)
            car.draw(screen)
            credits.draw(screen)
        elif game_state == SIMULATION:
            road.draw(screen)
            car.draw(screen)
        elif game_state == EXPLORATION:
            exploration.draw(screen)
        elif game_state == FREE_LAB:
            free_lab.draw(screen)
        elif game_state == MULTIPLAYER:
            multiplayer.draw(screen)
        elif game_state == TARGET_CHALLENGE:
            target_challenge.draw(screen)
        elif game_state == RESULT:
            road.draw(screen)
            car.draw(screen)
            result.draw(screen, question.score)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())