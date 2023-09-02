import pygame

pygame.init()
SIZE = W, H = 600, 600
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Крестики-нолики")
BOARD_SIZE = 3  # размер доски 3х3
TILE_SIZE = int(SIZE[0] / BOARD_SIZE)  # размер клетки
BLACK = (0, 0, 0)
CROSS_WIDTH = 25
LINE_WIDTH = 5
FONT_SIZE = 50
board = [[None] * BOARD_SIZE for i in range(BOARD_SIZE)]


def draw_board():
    SCREEN.fill((255, 255, 255))
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(SCREEN, BLACK, (0, i * TILE_SIZE), (SIZE[0], i * TILE_SIZE), LINE_WIDTH)  # рисуем поле для игр
        pygame.draw.line(SCREEN, BLACK, (i * TILE_SIZE, 0), (i * TILE_SIZE, SIZE[0]), LINE_WIDTH)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 'X':
                pygame.draw.line(SCREEN, BLACK, (i * TILE_SIZE + CROSS_WIDTH, j * TILE_SIZE + CROSS_WIDTH),
                                 ((i + 1) * TILE_SIZE - CROSS_WIDTH, (j + 1) * TILE_SIZE - CROSS_WIDTH), CROSS_WIDTH)
                pygame.draw.line(SCREEN, BLACK, ((i + 1) * TILE_SIZE - CROSS_WIDTH, j * TILE_SIZE + CROSS_WIDTH),
                                 (i * TILE_SIZE + CROSS_WIDTH, (j + 1) * TILE_SIZE - CROSS_WIDTH), CROSS_WIDTH)
                # рисуем крестик
            elif board[i][j] == 'O':
                pygame.draw.circle(SCREEN, BLACK,
                                   (int(i * TILE_SIZE + TILE_SIZE / 2), int(j * TILE_SIZE + TILE_SIZE / 2)),
                                   int(TILE_SIZE / 2 - 15), 15)

                # рисуем нолик


def winners():
    for i in range(BOARD_SIZE):
        if (board[i][0] == board[i][1] == board[i][2]) and board[i][0]:
            return board[i][0]
        if (board[0][i] == board[1][i] == board[2][i]) and board[0][i]:
            return board[0][i]
    if (board[0][0] == board[1][1] == board[2][2]) and board[0][0]:
        return board[0][0]
    if (board[0][2] == board[1][1] == board[2][0]) and board[0][2]:
        return board[0][2]
    return


def main():
    symbol = 'X'
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                tile_x = x // TILE_SIZE
                tile_y = y // TILE_SIZE
                if board[tile_x][tile_y] is None:  # если клетка доски пустая
                    board[tile_x][tile_y] = symbol
                    if symbol == 'X':
                        symbol = 'O'
                    else:
                        symbol = 'X'
        draw_board()
        winner = winners()
        if winner:
            SCREEN.fill((255, 255, 255))
            SCREEN.blit(font.render(f"{winner} wins", True, BLACK), (SIZE[0] / 2 - FONT_SIZE, SIZE[1] / 2 - FONT_SIZE))
            pygame.display.update()
            pygame.time.wait(1500)
            return
        elif all([all(row) for row in board]) and winner is None: # в случае, если никто не выиграл
            SCREEN.fill((255, 255, 255))
            SCREEN.blit(font.render("Friendship won", True, BLACK), (SIZE[0] / 2 - 120, SIZE[1] / 2 - FONT_SIZE))
            pygame.display.update()
            pygame.time.wait(1500)
            return
        pygame.display.update()


if __name__ == "__main__":
    main()