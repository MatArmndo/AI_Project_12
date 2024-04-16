import pygame
import math


class Bullet:
    def __init__(self, x, y, width, height, speed, color):
        self.rect = pygame.Rect(x - width // 2, y - height, width, height)
        self.speed = speed
        self.color = color
        self.laser_active = False
        self.remove = False  # Flag to indicate if the bullet should be removed
        self.laser_start_time = 0
        self.laser_duration = 300
        self.laser_end_y = 0

    def move(self):

        if not self.laser_active:
            self.rect.y -= self.speed
            self.laser_active = False
        else:
            self.rect.y = self.laser_end_y
            if pygame.time.get_ticks() - self.laser_start_time >= self.laser_duration:
                self.laser_active = False
        if self.rect.y < 0:
            self.remove = True  # Set the flag to True if the bullet has left the screen

    def draw(self, screen):
        if not self.laser_active:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.line(screen, self.color,
                             (self.rect.x + self.rect.width // 2, 0),
                             (self.rect.x, 601), 5)

    def change_color(self, color):
        self.color = color

    def apply_upgrade(self, upgrade_type, bullet_size_multiplier=None, bullet_speed_multiplier=None,
                      apply_to_current=False):
        if upgrade_type == "RED":
            bullet_size_multiplier[self.color] = 2.5
        elif upgrade_type == "GREEN":
            None
        elif upgrade_type == "BLUE" and apply_to_current:
            self.laser_active = True
            self.laser_start_time = pygame.time.get_ticks()  # Start tracking laser activation time
        elif upgrade_type == "YELLOW":
            bullet_speed_multiplier[self.color] = 5
        print(self.laser_active)
