import sys
import time

import pygame

import tictactoe as ttt

pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")

black = (0, 0, 0)
white = (255, 255, 255)

largeFont = pygame.font.SysFont("arial", 36)
mediumFont = pygame.font.SysFont("arial", 24)
moveFont = pygame.font.SysFont("arial", 48)


def main():
    user = None
    board = ttt.initial_state()
    ai_turn = False

    while True:
        handle_quit()
        screen.fill(black)

        if user is None:
            draw_menu()
            user = handle_menu_click(user)
        else:
            tiles = draw_board(board)
            game_over = ttt.terminal(board)
            player = ttt.player(board)

            draw_title(get_title_text(user, player, board, game_over))

            if not game_over:
                board, ai_turn = handle_ai_move(board, user, player, ai_turn)
                board = handle_user_move(board, user, player, tiles)
            else:
                if handle_play_again():
                    user, board, ai_turn = reset_game()

        pygame.display.flip()


# ------------------ HELPERS ------------------


def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# -------- MENU --------


def draw_menu():
    title = largeFont.render("Play Tic-Tac-Toe", True, white)
    screen.blit(title, title.get_rect(center=(WIDTH / 2, 50)))

    draw_button("Play as X", WIDTH / 8)
    draw_button("Play as O", 5 * WIDTH / 8)


def draw_button(text, x):
    button = pygame.Rect(x, HEIGHT / 2, WIDTH / 4, 50)
    pygame.draw.rect(screen, white, button)
    label = mediumFont.render(text, True, black)
    screen.blit(label, label.get_rect(center=button.center))


def handle_menu_click(user):
    if pygame.mouse.get_pressed()[0]:
        mouse = pygame.mouse.get_pos()
        if pygame.Rect(WIDTH / 8, HEIGHT / 2, WIDTH / 4, 50).collidepoint(mouse):
            time.sleep(0.2)
            return ttt.X
        if pygame.Rect(5 * WIDTH / 8, HEIGHT / 2, WIDTH / 4, 50).collidepoint(mouse):
            time.sleep(0.2)
            return ttt.O
    return user


# -------- BOARD --------


def draw_board(board):
    size = 80
    origin = (WIDTH / 2 - 1.5 * size, HEIGHT / 2 - 1.5 * size)
    tiles = []

    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(
                origin[0] + j * size,
                origin[1] + i * size,
                size,
                size,
            )
            pygame.draw.rect(screen, white, rect, 3)

            if board[i][j] is not None:
                move = moveFont.render(board[i][j], True, white)
                screen.blit(move, move.get_rect(center=rect.center))

            row.append(rect)
        tiles.append(row)

    return tiles


# -------- TITLE --------


def get_title_text(user, player, board, game_over):
    if game_over:
        winner = ttt.winner(board)
        return "Game Over: Tie." if winner is None else f"Game Over: {winner} wins."
    return f"Play as {user}" if user == player else "Computer thinking..."


def draw_title(text):
    title = largeFont.render(text, True, white)
    screen.blit(title, title.get_rect(center=(WIDTH / 2, 30)))


# -------- AI --------


def handle_ai_move(board, user, player, ai_turn):
    if user != player:
        if ai_turn:
            time.sleep(0.5)
            board = ttt.result(board, ttt.minimax(board))
            return board, False
        return board, True
    return board, ai_turn


# -------- USER MOVE --------


def handle_user_move(board, user, player, tiles):
    if pygame.mouse.get_pressed()[0] and user == player:
        mouse = pygame.mouse.get_pos()
        for i in range(3):
            for j in range(3):
                if board[i][j] is None and tiles[i][j].collidepoint(mouse):
                    return ttt.result(board, (i, j))
    return board


# -------- RESET --------


def handle_play_again():
    button = pygame.Rect(WIDTH / 3, HEIGHT - 65, WIDTH / 3, 50)
    pygame.draw.rect(screen, white, button)
    label = mediumFont.render("Play Again", True, black)
    screen.blit(label, label.get_rect(center=button.center))

    if pygame.mouse.get_pressed()[0] and button.collidepoint(pygame.mouse.get_pos()):
        time.sleep(0.2)
        return True
    return False


def reset_game():
    return None, ttt.initial_state(), False


# ------------------ RUN ------------------


if __name__ == "__main__":
    main()
