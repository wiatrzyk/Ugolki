import pygame
from game import Game
from ai import AI
import logging
import datetime

# logs_filename = str(datetime.datetime.now()).replace(":", ".")
logging.getLogger().setLevel(logging.DEBUG)
# logging.basicConfig(filename=f'logs/{logs_filename}',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)
# logging.debug('New Game')

WIN_WIDTH, WIN_HEIGHT = 1200, 800
BOARD_WIDTH = 640
PAWN_WIDTH = BOARD_WIDTH / 8
BOARD_COORDINATES = (280, 80)
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
FPS = 60

"""Loads graphics and sounds to memory"""
pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
icon = pygame.image.load('media/pawn_1.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Ugolki")
pawn1 = pygame.image.load('media/pawn_1.png')
pawn2 = pygame.image.load('media/pawn_2.png')
pawn1_big = pygame.image.load('media/pawn_1_big.png')
pawn2_big = pygame.image.load('media/pawn_2_big.png')
board = pygame.image.load('media/board_blue.png')
menu_board = pygame.image.load('media/main_window2.png')
button_image = pygame.image.load('media/button.png')
pawns = [pawn1, pawn2]
wait_image = pygame.image.load('media/dog.png')


def start():
    pygame.init()
    draw_window()


def draw_window():
    WINDOW.fill((85, 85, 85))
    WINDOW.blit(board, BOARD_COORDINATES)
    WINDOW.blit(pawn2_big, (40, 200))
    WINDOW.blit(pawn1_big, (940, 200))
    WINDOW.blit(button_image, (520, 730))


def draw_pawns(game_board):
    for row in range(8):
        for column in range(8):
            if game_board[row][column] != 0:
                WINDOW.blit(pawns[game_board[row][column] - 1],
                            (BOARD_COORDINATES[0] + PAWN_WIDTH * row, BOARD_COORDINATES[1] + PAWN_WIDTH * column))


def draw_stats(game):
    player1_points = font.render(f"{game.player1_score}/16", False, (0, 0, 0))
    player2_points = font.render(f"{game.player2_score}/16", False, (0, 0, 0))
    WINDOW.blit(player1_points, (1030, 450))
    WINDOW.blit(player2_points, (100, 450))


def draw_wait():
    WINDOW.blit(wait_image, (430, 220))


def click_on_board(click_coordinates) -> bool:
    if click_coordinates[0] > BOARD_COORDINATES[0]:
        if click_coordinates[0] < BOARD_COORDINATES[0] + BOARD_WIDTH:
            if click_coordinates[1] > BOARD_COORDINATES[1]:
                if click_coordinates[1] < BOARD_COORDINATES[1] + BOARD_WIDTH:
                    return True
    return False


def coordinates_to_board_squares(coordinates) -> list:
    result = []
    for i in range(2):
        value = int((coordinates[i] - BOARD_COORDINATES[i]) / PAWN_WIDTH)
        if value not in range(0, 8):
            return None
        result.append(value)
    return result


def game_loop():
    pygame.init()
    clock = pygame.time.Clock()
    game = Game()
    run = True
    while run:
        clock.tick(FPS)
        draw_window()
        draw_pawns(game.board)
        draw_stats(game)
        WINDOW.blit(font.render(f"Ruch gracza", False, (0, 0, 0)), (60, 730))
        if game.turn % 2:
            WINDOW.blit(pawn2, (250, 720))
        else:
            WINDOW.blit(pawn1, (250, 720))
        pygame.display.update()
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position_start = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_position_end = pygame.mouse.get_pos()

                    start_position = coordinates_to_board_squares(mouse_position_start)
                    end_position = coordinates_to_board_squares(mouse_position_end)
                    if start_position is not None and end_position is not None:
                        logging.debug(f"User move: {start_position}, {end_position}")
                        game.move(start_position, end_position)
                    else:
                        # next turn button
                        if mouse_position_start[0] in range(520, 680) and mouse_position_end[0] in range(520, 680):
                            if mouse_position_start[1] in range(730, 790) and mouse_position_end[1] in range(730, 790):
                                game.next_turn()

            if game.check_end():
                run = False
                WINDOW.fill((85, 85, 85))
                WINDOW.blit(pawn2_big, (500, 300))
                WINDOW.blit(pawn1_big, (800, 300))
                pygame.display.update()
                break

        except Exception as exc:
            logging.error(exc, exc_info=True)
    menu()


def game_loop_vs_ai():
    clock = pygame.time.Clock()
    game = Game()
    run = True
    while run:
        clock.tick(FPS)

        draw_window()
        draw_pawns(game.board)
        draw_stats(game)
        WINDOW.blit(font.render(f"Ruch gracza", False, (0, 0, 0)), (60, 730))
        if game.turn % 2:
            WINDOW.blit(pawn2, (250, 720))
        else:
            WINDOW.blit(pawn1, (250, 720))
        pygame.display.update()

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position_start = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_position_end = pygame.mouse.get_pos()

                    start_position = coordinates_to_board_squares(mouse_position_start)
                    end_position = coordinates_to_board_squares(mouse_position_end)
                    if start_position is not None and end_position is not None:
                        logging.debug(f"User move: {start_position}, {end_position}")
                        game.move(start_position, end_position)
                    else:
                        # next turn button
                        if mouse_position_start[0] in range(520, 680) and mouse_position_end[0] in range(520, 680):
                            if mouse_position_start[1] in range(730, 790) and mouse_position_end[1] in range(730, 790):
                                game.next_turn()

            if game.check_end():
                run = False
                WINDOW.fill((85, 85, 85))
                WINDOW.blit(pawn2_big, (500, 300))
                WINDOW.blit(pawn1_big, (800, 300))
                pygame.display.update()
                break
            else:
                if game.turn % 2 == 0:
                    logging.debug("AI turn")
                    draw_window()
                    draw_pawns(game.board)
                    draw_stats(game)
                    draw_wait()
                    pygame.display.update()
                    game = AI.make_move(game)

        except Exception as exc:
            logging.error(exc, exc_info=True)
    menu()


def game_loop_ai_vs_ai():
    pygame.init()
    clock = pygame.time.Clock()
    game = Game()
    run = True
    while run:
        clock.tick(FPS)

        draw_window()
        draw_pawns(game.board)
        draw_stats(game)
        WINDOW.blit(font.render(f"Ruch gracza", False, (0, 0, 0)), (60, 730))
        if game.turn % 2:
            WINDOW.blit(pawn2, (250, 720))
        else:
            WINDOW.blit(pawn1, (250, 720))
        pygame.display.update()

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if game.check_end():
                run = False
                WINDOW.fill((85, 85, 85))
                WINDOW.blit(pawn2_big, (500, 300))
                WINDOW.blit(pawn1_big, (800, 300))
                pygame.display.update()
                break
            elif run:
                player = 1 if game.turn % 2 == 0 else 2
                game = AI.make_move(game, player)

        except Exception as exc:
            logging.error(exc, exc_info=True)
    menu()


def menu():
    pygame.init()
    WINDOW.fill((85, 85, 85))
    WINDOW.blit(menu_board, (0, 0))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position_start = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position_end = pygame.mouse.get_pos()

                if mouse_position_start[0] in range(450, 750) and mouse_position_end[0] in range(450, 750):
                    if mouse_position_start[1] in range(155, 235) and mouse_position_end[1] in range(155, 235):
                        game_loop()

                if mouse_position_start[0] in range(450, 750) and mouse_position_end[0] in range(450, 750):
                    if mouse_position_start[1] in range(270, 350) and mouse_position_end[1] in range(270, 350):
                        game_loop_vs_ai()

                if mouse_position_start[0] in range(450, 750) and mouse_position_end[0] in range(450, 750):
                    if mouse_position_start[1] in range(385, 465) and mouse_position_end[1] in range(385, 465):
                        game_loop_ai_vs_ai()

                if mouse_position_start[0] in range(450, 750) and mouse_position_end[0] in range(450, 750):
                    if mouse_position_start[1] in range(495, 575) and mouse_position_end[1] in range(495, 575):
                        run = False


if __name__ == "__main__":
    menu()
    pygame.quit()
