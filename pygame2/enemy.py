import pygame
import random

class Enemy:
    def __init__(self, screen_width, size):
        self.rect = pygame.Rect(random.randint(0, screen_width - size), 0, size, size)
        self.color = random.choice([(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)])  # Red, Blue, Green, Yellow
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
