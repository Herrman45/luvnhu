import pygame
import random
import sys
import math

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sandworm Run")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND = (194, 178, 128)
RED = (255, 0, 0)
WORM = (252,232,131)
YELLOW = (255, 255, 0)

font = pygame.font.Font(None, 36)

def reset_game():
    global player_pos, score, spice_pos, sandworms
    player_size = 40
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    player_speed = 5
    score = 0
    spice_size = 20
    spice_pos = [random.randint(0, SCREEN_WIDTH - spice_size), random.randint(0, SCREEN_HEIGHT - spice_size)]
    sandworms = create_sandworms(1)

def create_sandworms(num_sandworms):
    sandworms = []
    for _ in range(num_sandworms):
        x, y = random.randint(0, SCREEN_WIDTH - 60), random.randint(0, SCREEN_HEIGHT - 60)
        target_x, target_y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        sandworms.append({'pos': [x, y], 'target': [target_x, target_y], 'speed': min(round(math.sqrt(2*score) + 2),9)})
    return sandworms

player_size = 40
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
score = 0
spice_size = 20
spice_pos = [random.randint(0, SCREEN_WIDTH - spice_size), random.randint(0, SCREEN_HEIGHT - spice_size)]
sandworms = create_sandworms(1)

directions = {
    pygame.K_LEFT: (-player_speed, 0),
    pygame.K_RIGHT: (player_speed, 0),
    pygame.K_UP: (0, -player_speed),
    pygame.K_DOWN: (0, player_speed),
}

def update_player_position(player_pos, direction):
    new_x = player_pos[0] + direction[0]
    new_y = player_pos[1] + direction[1]
    new_x = max(0, min(new_x, SCREEN_WIDTH - player_size))
    new_y = max(0, min(new_y, SCREEN_HEIGHT - player_size))
    return [new_x, new_y]

def check_collision(player_pos, sandworm_pos):
    px, py = player_pos
    sx, sy = sandworm_pos
    return (px + player_size > sx and px < sx + 60 and
            py + player_size > sy and py < sy + 60)

def check_spice_collection(player_pos, spice_pos):
    px, py = player_pos
    sx, sy = spice_pos
    return (px + player_size > sx and px < sx + spice_size and
            py + player_size > sy and py < sy + spice_size)

def move_sandworms(sandworms):
    for sandworm in sandworms:
        sx, sy = sandworm['pos']
        tx, ty = sandworm['target']
        dx = tx - sx
        dy = ty - sy
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx /= distance
            dy /= distance
            sx += dx * sandworm['speed']
            sy += dy * sandworm['speed']
        sandworm['pos'] = [sx, sy]
        if distance < 5:
            sandworm['target'] = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]

def game_loop():
    global player_pos, score, spice_pos, sandworms
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(SAND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        for key, direction in directions.items():
            if keys[key]:
                player_pos = update_player_position(player_pos, direction)
        for sandworm in sandworms:
            if check_collision(player_pos, sandworm['pos']):
                draw_text("Game Over! Press R to restart or Q to quit", RED, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                pygame.display.flip()
                game_over = True
                while game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_over = False
                            running = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_over = False
                                running = False
                            elif event.key == pygame.K_r:
                                reset_game()
                                game_over = False
                                game_loop()
                break
        if check_spice_collection(player_pos, spice_pos):
            score += 1
            spice_pos = [random.randint(0, SCREEN_WIDTH - spice_size), random.randint(0, SCREEN_HEIGHT - spice_size)]
            if score in [2,3,5,8,9,12]:
                sandworms.extend(create_sandworms(1))
        move_sandworms(sandworms)
        pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], player_size, player_size))
        pygame.draw.circle(screen, YELLOW, (spice_pos[0] + spice_size // 2, spice_pos[1] + spice_size // 2), spice_size // 2)
        for sandworm in sandworms:
            pygame.draw.rect(screen, WORM, (sandworm['pos'][0], sandworm['pos'][1], 60, 60))
        draw_text(f"Score: {score}", BLACK, 10, 10)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

def draw_text(text, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

game_loop()

