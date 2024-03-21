import pygame
import random
import math

class NPC:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = random.uniform(5 * 0.8, 5 * 1.2)  # Between 80% and 120% of player speed
        self.direction = random.uniform(0, 2 * math.pi)

    def draw(self, screen):
        '''Draws the NPC circle with a black outline, color filling, and centered name text.'''
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius + 4)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        font_size = max(int(self.radius // 2), 12)
        font = pygame.font.SysFont('Arial', font_size)
        text = font.render('NPC', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def move(self, screen_width, screen_height):
        '''Moves the NPC based on its speed and direction, checks for boundary collisions.'''
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        # Check for boundary collision
        if self.x <= self.radius + 4:
            self.x = self.radius + 4
            self.direction = random.uniform(0, 2 * math.pi)
        elif self.x >= screen_width - (self.radius + 4):
            self.x = screen_width - (self.radius + 4)
            self.direction = random.uniform(0, 2 * math.pi)
        if self.y <= self.radius + 4:
            self.y = self.radius + 4
            self.direction = random.uniform(0, 2 * math.pi)
        elif self.y >= screen_height - (self.radius + 4):
            self.y = screen_height - (self.radius + 4)
            self.direction = random.uniform(0, 2 * math.pi)

    def increase_size(self, consumed_radius):
        '''Adjusts NPC size after consuming a smaller circle or another NPC.'''
        original_area = math.pi * self.radius ** 2
        consumed_area = math.pi * consumed_radius ** 2
        new_area = original_area + consumed_area
        self.radius = math.sqrt(new_area / math.pi)

    def check_collision(self, other):
        '''Checks for collision with another NPC or the player.'''
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < self.radius + other.radius

    def consume_npc(self, consumed_radius):
        '''Allows for consuming another NPC, adjusting the NPC's size.'''
        self.increase_size(consumed_radius)

    def consume(self, small_circles):
        '''Consumes a SmallCircle, increasing the NPC's size accordingly.'''
        for circle in small_circles[:]:
            distance = math.sqrt((self.x - circle.x) ** 2 + (self.y - circle.y) ** 2)
            if distance < self.radius - circle.radius:
                small_circles.remove(circle)
                self.increase_size(circle.radius)