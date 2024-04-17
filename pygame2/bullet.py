import pygame

class Bullet:
    def __init__(self, x, y, color, size):
        self.size = size
        self.rect = pygame.Rect(x - self.size // 2, y, self.size, self.size * 2)
        self.color = color
        self.speed = 7

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
