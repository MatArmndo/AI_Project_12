import pygame
import sys
import random

from player import Player
from enemy import Enemy
from bullet import Bullet

import cv2
import numpy as np
from keras.models import load_model
from support_functions import *

# Set up the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Player Movement, Shooting, and Enemies")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Bullet variables
bullet_width = 5
bullet_height = 10
bullet_speed = 7
key_press_count = {pygame.K_1: 0, pygame.K_2: 0, pygame.K_3: 0, pygame.K_4: 0}  # Track key presses
power_up_activated = {RED: False, GREEN: False, BLUE: False,
                      YELLOW: False}  # Define boolean variables to track whether each power-up has been activated
bullet_size_multiplier = {RED: 1, GREEN: 1, BLUE: 1, YELLOW: 1}  # Multipliers for bullet sizes
bullet_speed_multiplier = {RED: 1, GREEN: 1, BLUE: 1, YELLOW: 1}  # Multipliers for bullet speed

# Load the trained model
model = load_model('trained_model_8classes.h5')

# Initialize Pygame
pygame.init()

# Function to predict label
def predict_label(grid):
    # Preprocess the grid
    grid = np.expand_dims(grid, axis=0)
    grid = np.expand_dims(grid, axis=-1)
    grid = grid / 255.0

    # Predict label
    prediction = model.predict(grid)
    predicted_label = np.argmax(prediction) + 1  # Classes start from 1

    return predicted_label

# Function to create enemies
def create_enemy(enemies, screen_width):
    if random.randint(1, 100) < 5:
        enemy_color = random.choice([RED, GREEN, BLUE, YELLOW])
        enemies.append(Enemy(20, 20, 3, enemy_color, screen_width))


# Main game loop
def main():
    player = Player(20, 20, WIDTH // 2, HEIGHT - 20, 5)
    bullets = []
    enemies = []
    current_bullet_color_index = 0
    score = 0
    game_over = False
    game_over_time = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                bullet_color = [RED, GREEN, BLUE, YELLOW][current_bullet_color_index]
                bullet_width_scaled = bullet_width * bullet_size_multiplier[bullet_color]
                bullet_height_scaled = bullet_height * bullet_size_multiplier[bullet_color]
                bullet_speed_scaled = bullet_speed * bullet_speed_multiplier[bullet_color]

                if event.key == pygame.K_SPACE and player.lives > 0:
                    bullets.append((Bullet(player.x, player.y, bullet_width_scaled, bullet_height_scaled,
                                           bullet_speed_scaled, bullet_color)))

                elif pygame.K_1 <= event.key <= pygame.K_4:
                    current_bullet_color_index = event.key - pygame.K_1

                elif pygame.K_5 <= event.key <= pygame.K_8:
                    upgrade_type = None
                    if event.key == pygame.K_5:
                        upgrade_type = "RED"
                    elif event.key == pygame.K_8:
                        upgrade_type = "YELLOW"
                    elif event.key == pygame.K_6:
                        upgrade_type = "BLUE"
                        bullet.apply_upgrade(upgrade_type, apply_to_current=True)
                    elif event.key == pygame.K_7:
                        upgrade_type = "GREEN"
                        new_bullets = []  # Store new bullets separately
                        new_bullets.extend(bullet.apply_upgrade(upgrade_type, bullet_size_multiplier,
                                                                bullet_speed_multiplier, apply_to_current=True))
                        bullets.extend(new_bullets)  # Add new bullets to the bullets list
                    for bullet in bullets:
                        bullet.apply_upgrade(upgrade_type, bullet_size_multiplier, bullet_speed_multiplier, apply_to_current=False)

                else:
                    # Reset bullet size multiplier to 1
                    for color in bullet_size_multiplier:
                        bullet_size_multiplier[color] = 1
                    for color in bullet_speed_multiplier:
                        bullet_speed_multiplier[color] = 1




        keys = pygame.key.get_pressed()
        player.move(keys, WIDTH)

        if not game_over:
            screen.fill(BLACK)
            player.draw(screen)

            for bullet in bullets:
                bullet.move()
                bullet.draw(screen)
                if bullet.remove:
                    bullets.remove(bullet)

            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)

            create_enemy(enemies, WIDTH)

            # Check for collisions between bullets and enemies
            for bullet in bullets:
                for enemy in enemies:
                    if bullet.rect.colliderect(enemy.rect) and bullet.color == enemy.color:
                        if bullet in bullets:
                            bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1  # Increment score when an enemy is destroyed

            # Check for collisions between player and enemies
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    player.lives -= 1
                    enemies.remove(enemy)


            # Draw score and player lives
            font = pygame.font.Font(None, 24)
            score_text = font.render(f"Score: {score}", True, WHITE)
            lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 30))

            if player.lives == 0:
                game_over_text = font.render("Game Over", True, WHITE)
                screen.blit(game_over_text, (
                WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
                game_over = True
                game_over_time = pygame.time.get_ticks()

            pygame.display.flip()
            pygame.time.Clock().tick(60)
        else:
            # Check if 5 seconds have passed since game over
            if pygame.time.get_ticks() - game_over_time >= 3000:  # 5000 milliseconds = 5 seconds
                break  # Exit the game loop

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
import pygame
import math
