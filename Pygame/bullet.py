import pygame

class Bullet:
    def __init__(self, x, y, width, height, speed, color):
        self.rect = pygame.Rect(x - width // 2, y - height, width, height)
        self.speed = speed
        self.color = color

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def change_color(self, color):
        self.color = color