import pygame
import random
from math import cos, sin, radians
from player import Player
from small_circle import SmallCircle

# Game window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
BACKGROUND_COLOR = (255, 255, 255) # White

def generate_random_color():
    '''Generates a random color'''
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Agar.io Clone')

    clock = pygame.time.Clock()
    running = True

    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 50, generate_random_color())
    small_circles = [SmallCircle(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), 10, generate_random_color())]

    def add_small_circle():
        '''Adds a new small circle in a random position near the player.'''
        angle = radians(random.randint(0, 360))
        distance = random.randint(0, 500)
        dx = int(cos(angle) * distance)
        dy = int(sin(angle) * distance)
        new_x = max(0, min(WINDOW_WIDTH, player.x + dx))
        new_y = max(0, min(WINDOW_HEIGHT, player.y + dy))
        new_circle = SmallCircle(new_x, new_y, 10, generate_random_color())
        small_circles.append(new_circle)
        
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type is pygame.USEREVENT + 1:
                add_small_circle()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -1)
        if keys[pygame.K_s]:
            player.move(0, 1)
        if keys[pygame.K_a]:
            player.move(-1, 0)
        if keys[pygame.K_d]:
            player.move(1, 0)

        player.consume(small_circles)

        screen.fill(BACKGROUND_COLOR)
        player.draw(screen)
        for circle in small_circles:
            circle.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()