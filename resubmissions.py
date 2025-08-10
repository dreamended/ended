import pygame
import random
import time

# Pygame initialization is handled here.
pygame.init()

# Game window dimensions. Space is allocated for a clean look with margins.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("happy move")

# Color definitions for drawing the tiles and the screen elements.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Font settings for score display.
# In case of failure, a fallback to a default font is provided to prevent a crash.
try:
    font = pygame.font.SysFont("simhei", 36)
except:
    font = pygame.font.Font(None, 36)

# Game board dimensions and positioning.
MARGIN = 50
BOARD_SIZE = 8
# Tile size is calculated based on screen width and margins to ensure a fit.
TILE_SIZE = (SCREEN_WIDTH - 2 * MARGIN) // BOARD_SIZE
board_start_x = MARGIN
board_start_y = MARGIN
# The game board's core data structure. A 2D grid initialized with random colors.
board = [[random.choice(COLORS) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Game state variables.
score = 0
selected_tile = None  # Tracks the currently selected tile.
is_swapping = False  # A state flag to prevent new actions during an animation.
swap_animation_timer = 0
swapping_r1, swapping_c1 = -1, -1  # Coordinates of the tiles being swapped.
swapping_r2, swapping_c2 = -1, -1


# A function to draw the entire game board.
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Coordinates for each tile are adjusted by the board's starting position.
            x = board_start_x + col * TILE_SIZE
            y = board_start_y + row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, board[row][col], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


# A function to draw the score on the screen.
def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (board_start_x, board_start_y + BOARD_SIZE * TILE_SIZE + 20))


# Core logic for finding matches of three or more tiles.
def check_matches():
    matches = []
    # Horizontal matches are checked.
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - 2):
            # A check confirms that three adjacent tiles have the same color and are not empty.
            if board[row][col] == board[row][col + 1] == board[row][col + 2] and board[row][col] is not None:
                match = [(row, col), (row, col + 1), (row, col + 2)]
                matches.append(match)
                # The check continues for longer matches (four or more tiles).
                for c in range(col + 3, BOARD_SIZE):
                    if board[row][c] == board[row][col]:
                        match.append((row, c))
                    else:
                        break
    # Vertical matches are checked with similar logic.
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] and board[row][col] is not None:
                match = [(row, col), (row + 1, col), (row + 2, col)]
                matches.append(match)
                for r in range(row + 3, BOARD_SIZE):
                    if board[r][col] == board[row][col]:
                        match.append((r, col))
                    else:
                        break
    return matches


# A function to remove matched tiles and update the score.
def remove_matches(matches):
    global score
    if not matches:
        return

    # A set is used to collect all matched tile coordinates to avoid duplicates.
    all_matched_coords = set()
    for match_group in matches:
        if len(match_group) >= 3:
            for coord in match_group:
                all_matched_coords.add(coord)

            # Score is assigned based on the number of tiles in the match.
            if len(match_group) == 3:
                score += 10
            elif len(match_group) == 4:
                score += 25
            elif len(match_group) >= 5:
                score += 50

    # The color of all matched tiles is set to None to mark them for removal.
    for row, col in all_matched_coords:
        board[row][col] = None


# A function to handle tile gravity and board refilling.
def fill_gaps():
    # Existing tiles are made to fall down to fill empty spaces.
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 1, -1, -1):
            if board[row][col] is None:
                for r in range(row - 1, -1, -1):
                    if board[r][col] is not None:
                        board[row][col] = board[r][col]
                        board[r][col] = None
                        break
    # Any remaining empty spots at the top of the board are filled with new random tiles.
    for col in range(BOARD_SIZE):
        for r in range(BOARD_SIZE):
            if board[r][col] is None:
                board[r][col] = random.choice(COLORS)


# The main game loop, which runs constantly.
running = True
clock = pygame.time.Clock()
while running:
    # Delta time is calculated to ensure smooth animations regardless of system speed.
    dt = clock.tick(60) / 1000.0

    # Player input is checked in this loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not is_swapping:
            mouse_pos = pygame.mouse.get_pos()
            # Mouse click coordinates are converted to board grid coordinates.
            col = (mouse_pos[0] - board_start_x) // TILE_SIZE
            row = (mouse_pos[1] - board_start_y) // TILE_SIZE

            if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
                # If a tile was previously selected, this click initiates a swap.
                if selected_tile:
                    r1, c1 = selected_tile
                    r2, c2 = row, col
                    if (abs(r1 - r2) + abs(c1 - c2) == 1):
                        is_swapping = True  # The swap animation begins.
                        swap_animation_timer = 0
                        swapping_r1, swapping_c1 = r1, c1
                        swapping_r2, swapping_c2 = r2, c2
                        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                    selected_tile = None
                else:
                    # If no tile was selected, this click selects the first tile.
                    selected_tile = (row, col)

    # The swap animation is handled here.
    if is_swapping:
        swap_animation_timer += dt
        animation_duration = 0.2

        if swap_animation_timer >= animation_duration:
            # Once the animation concludes, the swapping state is ended.
            is_swapping = False
            matches = check_matches()
            if matches:
                # If matches are found, they are removed and gaps are filled.
                remove_matches(matches)
                fill_gaps()
                # A loop checks for chain reactions, continuing until no new matches are found.
                while True:
                    new_matches = check_matches()
                    if new_matches:
                        remove_matches(new_matches)
                        fill_gaps()
                    else:
                        break
            else:
                # If no match is found, the tiles are swapped back to their original positions.
                board[swapping_r1][swapping_c1], board[swapping_r2][swapping_c2] = board[swapping_r2][swapping_c2], \
                    board[swapping_r1][swapping_c1]

    # --- Screen drawing logic ---
    screen.fill(WHITE)

    if not is_swapping:
        # If no animation is active, the board is drawn normally.
        draw_board()
    else:
        # During an animation, the moving tiles are drawn separately.
        t = swap_animation_timer / animation_duration

        # Start and end positions for the moving tiles are calculated.
        x1_start, y1_start = board_start_x + swapping_c1 * TILE_SIZE, board_start_y + swapping_r1 * TILE_SIZE
        x2_start, y2_start = board_start_x + swapping_c2 * TILE_SIZE, board_start_y + swapping_r2 * TILE_SIZE
        x1_end, y1_end = board_start_x + swapping_c2 * TILE_SIZE, board_start_y + swapping_r2 * TILE_SIZE
        x2_end, y2_end = board_start_x + swapping_c1 * TILE_SIZE, board_start_y + swapping_r1 * TILE_SIZE

        # Linear interpolation is used to determine the exact position of the tiles in transit.
        x1 = x1_start + (x1_end - x1_start) * t
        y1 = y1_start + (y1_end - y1_start) * t
        x2 = x2_start + (x2_end - x2_start) * t
        y2 = y2_end + (y2_end - y2_start) * t

        # All non-moving tiles are drawn first.
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row, col) not in [(swapping_r1, swapping_c1), (swapping_r2, swapping_c2)]:
                    rect = pygame.Rect(board_start_x + col * TILE_SIZE, board_start_y + row * TILE_SIZE, TILE_SIZE,
                                       TILE_SIZE)
                    pygame.draw.rect(screen, board[row][col], rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)

        # The colors for the moving tiles are retrieved.
        color1 = board[swapping_r2][swapping_c2]
        color2 = board[swapping_r1][swapping_c1]

        # The two moving tiles are drawn at their current interpolated positions.
        rect1 = pygame.Rect(x1, y1, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color1, rect1)
        rect2 = pygame.Rect(x2, y2, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color2, rect2)
        pygame.draw.rect(screen, BLACK, rect1, 1)
        pygame.draw.rect(screen, BLACK, rect2, 1)

    # The border around the currently selected tile is drawn.
    if selected_tile and not is_swapping:
        r, c = selected_tile
        pygame.draw.rect(screen, BLACK,
                         pygame.Rect(board_start_x + c * TILE_SIZE, board_start_y + r * TILE_SIZE, TILE_SIZE,
                                     TILE_SIZE), 3)

    draw_score()

    # The entire screen is updated to display the changes.
    pygame.display.flip()

# Pygame is quit when the main loop ends
pygame.quit()