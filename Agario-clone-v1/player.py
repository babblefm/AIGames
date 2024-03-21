import pygame
import math

class Player:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 2
    
    def draw(self, screen):
        '''Draws the player circle with a black outline.'''
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius + 4)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def move(self, dx, dy):
        '''Updates the player's position based on movement direction.'''
        self.x += dx * self.speed
        self.y += dy * self.speed

    def consume(self, small_circles):
        '''Checks for collision with small circles and consumes them if collision is detected.'''
        for circle in small_circles[:]:
            distance = math.sqrt((self.x - circle.x) ** 2 + (self.y - circle.y) ** 2)
            if distance < self.radius - circle.radius:
                small_circles.remove(circle)
                self.increase_size(circle.radius)

    def increase_size(self, consumed_radius):
        '''Increases the player's circle radius based on the radius of the consumed circle to maintain area sum.'''
        original_area = math.pi * self.radius**2
        consumed_area = math.pi * consumed_radius**2
        new_area = original_area + consumed_area
        self.radius = math.sqrt(new_area / math.pi)