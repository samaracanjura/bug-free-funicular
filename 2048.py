import pygame
import random
import math

pygame.init()

FPS = 60

WIDTH, HEIGHT = 800, 950
ROWS = 4
COLS = 4

SCORE_HEIGHT = 150
RECT_HEIGHT = (HEIGHT - SCORE_HEIGHT) // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (216, 191, 216)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (250, 235, 245)
FONT_COLOR = (99, 21, 80)
BUTTON_COLOR = (186, 85, 211)
BUTTON_HOVER_COLOR = (147, 112, 219)

FONT = pygame.font.SysFont("chalkboard", 60, bold=True)
SCORE_FONT = pygame.font.SysFont("chalkboard", 40, bold=True)
BUTTON_FONT = pygame.font.SysFont("chalkboard", 30, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
    
    def draw(self, window):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(window, color, self.rect, border_radius=10)
        
        text_surface = BUTTON_FONT.render(self.text, 1, (255, 255, 255))
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        window.blit(text_surface, (text_x, text_y))
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Tile:
    COLORS = [
        (255, 240, 245),  # Lavender blush
        (255, 228, 245),  # Light pink
        (255, 192, 203),  # Pink
        (255, 182, 193),  # Light pink
        (255, 160, 200),  # Bright pink
        (238, 130, 238),  # Violet
        (221, 160, 221),  # Plum
        (218, 112, 214),  # Orchid
        (186, 85, 211),   # Medium orchid
        (147, 112, 219),  # Medium purple
        (138, 43, 226),   # Blue violet
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT + SCORE_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil((self.y - SCORE_HEIGHT) / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor((self.y - SCORE_HEIGHT) / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT + SCORE_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, SCORE_HEIGHT), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, SCORE_HEIGHT, WIDTH, HEIGHT - SCORE_HEIGHT), OUTLINE_THICKNESS)


def draw_score(window, score):
    score_text = SCORE_FONT.render(f"Score: {score}", 1, FONT_COLOR)
    window.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, 30)
    )


def draw_game_over(window):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))
    
    game_over_text = SCORE_FONT.render("Game Over!", 1, (255, 255, 255))
    restart_text = BUTTON_FONT.render("Click Restart to play again", 1, (255, 255, 255))
    
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))


def draw_buttons(window, restart_button, quit_button):
    restart_button.draw(window)
    quit_button.draw(window)


def draw(window, tiles, score, restart_button, quit_button, game_over=False):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)
    draw_score(window, score)
    draw_buttons(window, restart_button, quit_button)
    
    if game_over:
        draw_game_over(window)

    pygame.display.update()


def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def has_valid_moves(tiles):
    """Check if there are any valid moves remaining"""
    # If board is not full, there are valid moves
    if len(tiles) < 16:
        return True
    
    # Check for adjacent tiles with same value (horizontal and vertical)
    for row in range(ROWS):
        for col in range(COLS):
            current_tile = tiles.get(f"{row}{col}")
            if not current_tile:
                continue
            
            # Check right neighbor
            if col < COLS - 1:
                right_tile = tiles.get(f"{row}{col + 1}")
                if right_tile and current_tile.value == right_tile.value:
                    return True
            
            # Check down neighbor
            if row < ROWS - 1:
                down_tile = tiles.get(f"{row + 1}{col}")
                if down_tile and current_tile.value == down_tile.value:
                    return True
    
    return False


def move_tiles(window, tiles, clock, direction, score, restart_button, quit_button):
    updated = True
    blocks = set()
    score_increase = 0

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    score_increase += next_tile.value
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles, score + score_increase, restart_button, quit_button)

    end_result = end_move(tiles)
    return end_result, score_increase


def end_move(tiles):
    """Spawn a new tile and check game over conditions"""
    # Spawn new tile with correct probability: 90% = 2, 10% = 4
    row, col = get_random_pos(tiles)
    new_value = 2 if random.random() < 0.9 else 4
    tiles[f"{row}{col}"] = Tile(new_value, row, col)
    
    # Check if game is over (no valid moves remaining)
    if not has_valid_moves(tiles):
        return "lost"
    
    return "continue"


def update_tiles(window, tiles, sorted_tiles, score, restart_button, quit_button):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles, score, restart_button, quit_button)


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main(window, seed=None):
    # Determinism hook: set random seed for reproducible gameplay
    if seed is not None:
        random.seed(seed)
    
    clock = pygame.time.Clock()
    run = True
    score = 0
    game_over = False

    # Create buttons
    button_width = 150
    button_height = 40
    button_y = 90
    spacing = 20
    total_width = button_width * 2 + spacing
    start_x = (WIDTH - total_width) // 2
    
    restart_button = Button(start_x, button_y, button_width, button_height, "Restart")
    quit_button = Button(start_x + button_width + spacing, button_y, button_width, button_height, "Quit")

    tiles = generate_tiles()

    while run:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        restart_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(mouse_pos):
                    tiles = generate_tiles()
                    score = 0
                    game_over = False
                elif quit_button.is_clicked(mouse_pos):
                    run = False
                    break

            if event.type == pygame.KEYDOWN and not game_over:
                result = None
                points = 0
                
                # Arrow keys
                if event.key == pygame.K_LEFT:
                    result, points = move_tiles(window, tiles, clock, "left", score, restart_button, quit_button)
                elif event.key == pygame.K_RIGHT:
                    result, points = move_tiles(window, tiles, clock, "right", score, restart_button, quit_button)
                elif event.key == pygame.K_UP:
                    result, points = move_tiles(window, tiles, clock, "up", score, restart_button, quit_button)
                elif event.key == pygame.K_DOWN:
                    result, points = move_tiles(window, tiles, clock, "down", score, restart_button, quit_button)
                # WASD keys
                elif event.key == pygame.K_a:
                    result, points = move_tiles(window, tiles, clock, "left", score, restart_button, quit_button)
                elif event.key == pygame.K_d:
                    result, points = move_tiles(window, tiles, clock, "right", score, restart_button, quit_button)
                elif event.key == pygame.K_w:
                    result, points = move_tiles(window, tiles, clock, "up", score, restart_button, quit_button)
                elif event.key == pygame.K_s:
                    result, points = move_tiles(window, tiles, clock, "down", score, restart_button, quit_button)
                
                if result:
                    score += points
                    if result == "lost":
                        game_over = True

        draw(window, tiles, score, restart_button, quit_button, game_over)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)