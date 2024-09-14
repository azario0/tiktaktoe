import pygame
import sys
# Initialize Pygame
pygame.init()
# Constants
WIDTH, HEIGHT = 450, 450
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
# RGB Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)
# Board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def is_winner(player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full():
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells():
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def alpha_beta(depth, alpha, beta, maximizing_player):
    if is_winner('O'):
        return 1
    if is_winner('X'):
        return -1
    if is_full():
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells():
            board[i][j] = 'O'
            eval = alpha_beta(depth + 1, alpha, beta, False)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_empty_cells():
            board[i][j] = 'X'
            eval = alpha_beta(depth + 1, alpha, beta, True)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move():
    best_val = float('-inf')
    best_move = None
    for i, j in get_empty_cells():
        board[i][j] = 'O'
        move_val = alpha_beta(0, float('-inf'), float('inf'), False)
        board[i][j] = ' '
        if move_val > best_val:
            best_move = (i, j)
            best_val = move_val
    return best_move

def reset_game():
    global board
    screen.fill(BG_COLOR)
    draw_lines()
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    pygame.display.update()

def display_end_screen(message):
    screen.fill((0, 0, 0))  # Black screen
    font = pygame.font.Font(None, 40)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH/2, 30))
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 32)
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT - 30))
    screen.blit(restart_text, restart_rect)
    
    pygame.display.update()

def main():
    game_over = False
    player_turn = True  # True for player (X), False for AI (O)

    draw_lines()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    clicked_row = int(mouseY // SQUARE_SIZE)
                    clicked_col = int(mouseX // SQUARE_SIZE)

                    if board[clicked_row][clicked_col] == ' ':
                        board[clicked_row][clicked_col] = 'X'
                        player_turn = False

                        if is_winner('X'):
                            game_over = True
                            display_end_screen("You win!")
                        elif is_full():
                            game_over = True
                            display_end_screen("It's a tie!")

            if not player_turn and not game_over:
                row, col = get_best_move()
                board[row][col] = 'O'
                player_turn = True

                if is_winner('O'):
                    game_over = True
                    display_end_screen("You lose!")
                elif is_full():
                    game_over = True
                    display_end_screen("It's a tie!")

            if not game_over:
                draw_figures()
                pygame.display.update()

            if game_over:
                waiting_for_key = True
                while waiting_for_key:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                reset_game()
                                game_over = False
                                player_turn = True
                                waiting_for_key = False
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    main()