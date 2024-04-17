import pygame
import math


class Bullet:
    def __init__(self, x, y, width, height, speed, color):
        self.rect = pygame.Rect(x - width // 2, y - height, width, height)
        self.speed = speed
        self.color = color
        self.laser_active = False
        self.AOE = False
        self.remove = False  # Flag to indicate if the bullet should be removed
        self.laser_start_time = 0
        self.laser_duration = 300
        self.laser_end_y = 0
        self.vx = 0  # x-component of velocity
        self.vy = 0  # y-component of velocity

    def move(self):

        self.rect.y -= self.speed  # Common movement for both laser and regular bullets
        if self.AOE:
            self.rect.x += self.vx  # Update x-coordinate based on x-component of velocity
            self.rect.y += self.vy  # Update y-coordinate based on y-component of velocity

        if not self.laser_active and not self.AOE:
            pass  # No extra actions needed for regular bullets

        elif self.laser_active:
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
            self.AOE = True
            new_bullets = []  # Create a list to store new bullets
            # Calculate angle increments for bullets in the arc
            angle_increment = math.pi / 12  # Adjust as needed for the desired arc shape
            start_angle = -math.pi / 6  # Start angle for the arc
            # Create three bullets in an arc pattern
            for i in range(3):
                # Calculate the angle for the current bullet
                angle = start_angle + i * angle_increment
                print("Angle:", angle)
                # Calculate bullet velocity components based on angle
                vx = self.speed * bullet_speed_multiplier[self.color] * math.sin(angle)
                vy = -self.speed * bullet_speed_multiplier[self.color] * math.cos(angle)
                print("Vx:", vx, "Vy:", vy)
                # Create a new bullet with adjusted velocity
                new_bullet = Bullet(self.rect.x + self.rect.width // 2, self.rect.y, self.rect.width, self.rect.height,
                                    self.speed, self.color)
                new_bullet.speed = math.sqrt(vx ** 2 + vy ** 2)
                new_bullet.vx = vx  # Store the x-component of velocity
                new_bullet.vy = vy  # Store the y-component of velocity
                new_bullets.append(new_bullet)  # Add the new bullet to the list
            return new_bullets

        elif upgrade_type == "BLUE" and apply_to_current:
            self.laser_active = True
            self.laser_start_time = pygame.time.get_ticks()  # Start tracking laser activation time
        elif upgrade_type == "YELLOW":
            bullet_speed_multiplier[self.color] = 5
