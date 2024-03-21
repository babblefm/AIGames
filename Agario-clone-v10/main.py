import pygame
import random
import math
from player import Player
from small_circle import SmallCircle
from npc import NPC

# Game window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
BACKGROUND_COLOR = (255, 255, 255)  # White

def generate_random_color():
    '''Generates a random color.'''
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_random_position(distance=500, min_radius=10):
    '''Generates a random position within the game window.'''
    x = random.randint(min_radius + 4, WINDOW_WIDTH - (min_radius + 4))
    y = random.randint(min_radius + 4, WINDOW_HEIGHT - (min_radius + 4))
    return x, y

def generate_random_position_near_player(player_x, player_y):
    '''Generates a random position within a 500 pixel distance of the player's circle in a random position.'''
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0, 500)
    x = player_x + radius * math.cos(angle)
    y = player_y + radius * math.sin(angle)
    x = max(14, min(WINDOW_WIDTH - 14, x))
    y = max(14, min(WINDOW_HEIGHT - 14, y))
    return int(x), int(y)

def check_npc_collisions(npcs):
    '''Check and handle collisions between NPCs, including consumption.'''
    for npc1 in npcs[:]:
        for npc2 in npcs[:]:
            if npc1 != npc2 and npc1.check_collision(npc2):
                if npc1.radius > npc2.radius:
                    npc1.consume_npc(npc2.radius)
                    npcs.remove(npc2)
                elif npc2.radius > npc1.radius:
                    npc2.consume_npc(npc1.radius)
                    npcs.remove(npc1)
                # If sizes are equal, nothing happens

def check_player_npc_collisions(player, npcs):
    '''Checks and handles collisions between player and NPCs.'''
    for npc in npcs[:]:
        if player.check_collision(npc):
            if player.radius > npc.radius:
                player.consume_npc(npc.radius)
                npcs.remove(npc)
            elif npc.radius > player.radius:
                pygame.quit()
                raise SystemExit("Game over. An NPC consumed the player.")

def add_npc(npcs):
    '''Adds a new NPC with random attributes to the game.'''
    x, y = generate_random_position()
    radius = 50  # Starting size for NPCs
    color = generate_random_color()
    npc = NPC(x, y, radius, color)
    npcs.append(npc)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Agar.io Clone')

    clock = pygame.time.Clock()
    running = True

    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 50, generate_random_color())
    small_circles = []
    npcs = []

    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # For small circles
    pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # For NPCs

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                x, y = generate_random_position_near_player(player.x, player.y)
                color = generate_random_color()
                circle = SmallCircle(x, y, 10, color)
                small_circles.append(circle)
            elif event.type == pygame.USEREVENT + 2:
                add_npc(npcs)

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1
        player.move(dx, dy, WINDOW_WIDTH, WINDOW_HEIGHT)
        player.consume(small_circles)
        
        for npc in npcs:
            npc.move(WINDOW_WIDTH, WINDOW_HEIGHT)
            npc.consume(small_circles)

        check_npc_collisions(npcs)
        check_player_npc_collisions(player, npcs)

        screen.fill(BACKGROUND_COLOR)
        # Drawing the grid
        for x in range(0, WINDOW_WIDTH, 50):
            pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, 50):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (WINDOW_WIDTH, y))
        player.draw(screen)
        for npc in npcs:
            npc.draw(screen)
        for circle in small_circles:
            circle.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()