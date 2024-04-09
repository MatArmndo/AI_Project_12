import pygame
import random

class Enemy:
    def __init__(self, width, height, speed, color, screen_width):
        self.width = width
        self.height = height
        self.x = random.randint(0, screen_width - width)
        self.y = 0
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Create a Rect object for collision detection

    def move(self):
        self.y += self.speed
        self.rect.y = self.y  # Update the y-coordinate of the Rect object

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
