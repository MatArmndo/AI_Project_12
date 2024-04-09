import pygame

class Player:
    def __init__(self, width, height, x, y, speed):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.lives = 5
        self.rect = pygame.Rect(x - width // 2, y - height, width, height)  # Create a Rect object for collision detection

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT] and self.x > self.width:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > self.height:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < screen_width - self.height:
            self.y += self.speed
        self.rect.x = self.x  # Update the x-coordinate of the Rect object
        self.rect.y = self.y  # Update the y-coordinate of the Rect object

    def draw(self, screen):
        if self.lives > 0:
            pygame.draw.polygon(screen, (255, 255, 255), [(self.x, self.y - self.height),
                                                           (self.x - self.width // 2, self.y + self.height),
                                                           (self.x + self.width // 2, self.y + self.height)])
