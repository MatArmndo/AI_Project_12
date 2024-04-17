from player import Player
from enemy import Enemy
from bullet import Bullet

import pygame
import sys
import random
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
current_bullet_color_index = 0  # Default bullet color index


key_press_count = {pygame.K_1: 0, pygame.K_2: 0, pygame.K_3: 0, pygame.K_4: 0}  # Track key presses
power_up_activated = {RED: False, GREEN: False, BLUE: False,
                      YELLOW: False}  # Define boolean variables to track whether each power-up has been activated
bullet_size_multiplier = {RED: 1, GREEN: 1, BLUE: 1, YELLOW: 1}  # Multipliers for bullet sizes
bullet_speed_multiplier = {RED: 1, GREEN: 1, BLUE: 1, YELLOW: 1}  # Multipliers for bullet speed

# Load the trained model
model = load_model('trained_model_8classes.h5')  # Replace with your trained model file

# Initialize TSPDecoder
rows = 27
columns = 19
TSP = TSPDecoder(rows=rows, columns=columns)

tot = np.zeros((rows, columns))


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
    score = 0
    game_over = False
    game_over_time = None

    running = True
    while running and TSPDecoder.available():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                # Predict label when 'v' key is pressed
                predicted_label = predict_label(tot)
                print("Predicted Label:", predicted_label)

                # Use the predicted label to determine bullet behavior
                bullet_color = [RED, GREEN, BLUE, YELLOW][predicted_label - 1]
                bullet_width_scaled = bullet_width
                bullet_height_scaled = bullet_height
                bullet_speed_scaled = bullet_speed

                # Fire bullets
                if player.lives > 0:
                    bullets.append((Bullet(player.x, player.y, bullet_width_scaled, bullet_height_scaled,
                                           bullet_speed_scaled, bullet_color)))

                # Change bullet color or apply upgrades based on the predicted label
                if 1 <= predicted_label <= 4:
                    current_bullet_color_index = predicted_label - 1
                elif 5 <= predicted_label <= 8:
                    upgrade_type = None
                    if predicted_label == 5:
                        upgrade_type = "RED"
                    elif predicted_label == 8:
                        upgrade_type = "YELLOW"
                    elif predicted_label == 6:
                        upgrade_type = "BLUE"
                        bullet.apply_upgrade(upgrade_type, apply_to_current=True)
                    elif predicted_label == 7:
                        upgrade_type = "GREEN"
                        new_bullets = []  # Store new bullets separately
                        new_bullets.extend(bullet.apply_upgrade(upgrade_type, bullet_size_multiplier,
                                                                bullet_speed_multiplier, apply_to_current=True))
                        bullets.extend(new_bullets)  # Add new bullets to the bullets list
                    for bullet in bullets:
                        bullet.apply_upgrade(upgrade_type, bullet_size_multiplier, bullet_speed_multiplier, apply_to_current=False)

                # Reset bullet size multiplier
                for color in bullet_size_multiplier:
                    bullet_size_multiplier[color] = 1
                for color in bullet_speed_multiplier:
                    bullet_speed_multiplier[color] = 1

        # Player movement
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

            # Drawing recognition code
            # Read frame from TSPDecoder
            grid = TSP.readFrame()
            tot = np.maximum(tot, grid)
            tmp = cv2.resize(tot, (rows * 10, columns * 10))

            # Show frame
            cv2.imshow("Drawing", tmp.astype(np.uint8))
            key = cv2.waitKey(1)

            # Handle key presses
            if key == ord('c'):
                tot = np.zeros((rows, columns))  # Clear the drawing


