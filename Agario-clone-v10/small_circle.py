import pygame

class SmallCircle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        '''Draws a small circle with a black outline at its position.'''
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius + 4)  # Black outline
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)  # Inner circle with the specified color