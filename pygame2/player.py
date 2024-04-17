import pygame

class Player:
    def __init__(self, screen_width, screen_height):
        self.size = 20  # smaller player size
        self.x = screen_width // 2  # start at the horizontal center of the screen
        self.y = screen_height - self.size  # start at the bottom of the screen
        self.speed = 5
        self.lives = 5  # initial player lifespan

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT] and self.x > self.size:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.size:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > self.size:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < screen_height - self.size:
            self.y += self.speed

    def draw(self, screen):
        if self.lives > 0:
            pygame.draw.polygon(screen, (255, 255, 255), [(self.x, self.y - self.size),
                                                           (self.x - self.size // 2, self.y + self.size),
                                                           (self.x + self.size // 2, self.y + self.size)])
