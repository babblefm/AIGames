import pygame
import math

class Player:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 5  # Adjusted speed for a better gameplay experience

    def draw(self, screen):
        '''Draws the player's circle with a black outline and a label.'''
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius + 4)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        font_size = max(int(self.radius // 2), 12)
        font = pygame.font.SysFont('Arial', font_size)
        text = font.render('Player', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def move(self, dx, dy, screen_width, screen_height):
        '''Updates the player's position based on the input direction, checking screen boundaries.'''
        self.x = max(self.radius + 4, min(screen_width - (self.radius + 4), self.x + dx * self.speed))
        self.y = max(self.radius + 4, min(screen_height - (self.radius + 4), self.y + dy * self.speed))

    def consume(self, small_circles):
        '''Checks for and handles the consumption of smaller circles by the player.'''
        for circle in small_circles[:]:
            distance = math.sqrt((self.x - circle.x) ** 2 + (self.y - circle.y) ** 2)
            if distance < self.radius - circle.radius:
                small_circles.remove(circle)
                self.increase_size(circle.radius)

    def consume_npc(self, npc_radius):
        '''Consumes an NPC, increasing the player's size accordingly.'''
        self.increase_size(npc_radius)

    def increase_size(self, consumed_radius):
        '''Calculates and applies the new size for the player after consuming a circle or NPC.'''
        original_area = math.pi * self.radius ** 2
        consumed_area = math.pi * consumed_radius ** 2
        new_area = original_area + consumed_area
        self.radius = math.sqrt(new_area / math.pi)

    def check_collision(self, npc):
        '''Checks for collision with an NPC.'''
        distance = math.sqrt((self.x - npc.x) ** 2 + (self.y - npc.y) ** 2)
        return distance < self.radius + npc.radius