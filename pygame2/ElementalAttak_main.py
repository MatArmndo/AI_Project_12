import pygame
import sys
import random
from player import Player
from bullet import Bullet
from enemy import Enemy

import cv2
from keras.models import load_model
from support_functions import *


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the screen dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Player Movement, Shooting, and Enemies")

    # Colors
    BLACK = (0, 0, 0)

    # Player
    player = Player(WIDTH, HEIGHT)

    # Bullets
    bullets = []
    bullet_color_options = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]  # Red, Blue, Green, Yellow
    current_bullet_color_index = 0  # Index to track the current bullet color
    bullet_size = 5
    bullet_color = bullet_color_options[current_bullet_color_index]  # Initialize the current bullet color

    # Enemies
    enemies = []

    # Load the trained model
    model = load_model('trained_model_8classes.h5')

    # TSP Decoder
    rows = 27
    columns = 19
    TSP = TSPDecoder(rows=rows, columns=columns)
    tot = np.zeros((rows, columns))
    predicted_label = None

    # Function to predict label
    def predict_label(grid):
        # Preprocess the grid
        grid = np.expand_dims(grid, axis=0)
        grid = np.expand_dims(grid, axis=-1)
        grid = grid / 255.0

        # Predict label
        prediction = model.predict(grid)
        predicted_label = np.argmax(prediction) + 1  # 클래스를 1부터 시작하도록 수정

        return predicted_label

    # Function to handle events
    def handle_events(current_bullet_color_index, bullet_size, bullet_color, predicted_label):
        # global predicted_label  # Declare predicted_label as global
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Change bullet color
            if predicted_label == 1:
                current_bullet_color_index = 0  # Red
            elif predicted_label == 2:
                current_bullet_color_index = 1  # Blue
            elif predicted_label == 3:
                current_bullet_color_index = 2  # Green
            elif predicted_label == 4:
                current_bullet_color_index = 3  # Yellow
            elif predicted_label == 5:
                current_bullet_color_index = 0  # Powered-up Red
                bullet_size = 10
            elif predicted_label == 6:
                current_bullet_color_index = 1  # Powered-up Blue
                bullet_size = 10
            elif predicted_label == 7:
                current_bullet_color_index = 2  # Powered-up Green
                bullet_size = 10
            elif predicted_label == 8:
                current_bullet_color_index = 3  # Powered-up Yellow
                bullet_size = 10
            bullet_color = bullet_color_options[current_bullet_color_index]

            # Player shooting
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.lives > 0:
                bullets.append(Bullet(player.x - 2, player.y - player.size, bullet_color, bullet_size))

        return current_bullet_color_index, bullet_size, bullet_color

    # Function to update game state
    def update():
        # Get the state of all keyboard keys
        keys = pygame.key.get_pressed()

        # Update player position based on key presses
        player.move(keys, WIDTH, HEIGHT)

        # Update bullet positions
        for bullet in bullets:
            bullet.move()

        # Remove bullets that have left the screen
        bullets[:] = [bullet for bullet in bullets if bullet.rect.y > 0]

        # Create new enemies randomly
        if random.randint(1, 100) < 5:
            enemies.append(Enemy(WIDTH, 20))  # Create a new enemy

        # Update enemy positions
        for enemy in enemies:
            enemy.move()

        # Check for collisions between bullets and enemies
        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect) and bullet.color == enemy.color:
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        # Check for collisions between player and enemies
        for enemy in enemies:
            if enemy.rect.colliderect(pygame.Rect(player.x - player.size // 2, player.y - player.size, player.size, player.size)):
                player.lives -= 1
                enemies.remove(enemy)

    # Function to draw objects on the screen
    def draw():
        # Clear the screen
        screen.fill(BLACK)

        # Draw player
        player.draw(screen)

        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Draw player lives
        font = pygame.font.Font(None, 24)
        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

        # Update the display
        pygame.display.flip()



    # Main game loop
    # running = True
    while TSP.available:
        update()  # Update game state
        draw()  # Draw objects on the screen

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
        elif key == ord('v'):
            # Predict label
            predicted_label = predict_label(tot)
            print("Predicted Label:", predicted_label)

        current_bullet_color_index, bullet_size, bullet_color = handle_events(current_bullet_color_index, bullet_size, bullet_color, predicted_label)  # Handle events


        # Cap the frame rate
        pygame.time.Clock().tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Run the main function
if __name__ == "__main__":
    main()
