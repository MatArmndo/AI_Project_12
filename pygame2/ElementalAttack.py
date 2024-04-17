import pygame
import sys
import random

# Initialize Pygame
pygame.init()

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

# Player properties
player_size = 20  # smaller player size
player_x = WIDTH // 2  # start at the horizontal center of the screen
player_y = HEIGHT - player_size  # start at the bottom of the screen
player_speed = 5
player_lives = 5  # initial player lifespan

# Bullet properties
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []
bullet_color_options = [RED, BLUE, GREEN, YELLOW]  # Red, Blue, Green, Yellow
current_bullet_color_index = 0  # Index to track the current bullet color

# Enemy properties
enemy_size = 20
enemy_speed = 3
enemy_color_options = [RED, BLUE, GREEN, YELLOW]  # Red, Blue, Green, Yellow

enemies = []

# Function to create a new enemy
def create_enemy():
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = 0
    enemy_color = random.choice(enemy_color_options)  # Choose a random color for the enemy
    enemies.append((pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size), enemy_color))  # Append a tuple containing enemy rect and color

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player shooting
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_lives > 0:
            bullet_color = bullet_color_options[current_bullet_color_index]
            bullets.append((pygame.Rect(player_x - bullet_width // 2, player_y - player_size, bullet_width, bullet_height), bullet_color))

        # Change bullet color
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            current_bullet_color_index = 0  # Red
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            current_bullet_color_index = 1  # Blue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            current_bullet_color_index = 2  # Green
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            current_bullet_color_index = 3  # Yellow

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Update player position based on key presses
    if keys[pygame.K_LEFT] and player_x > player_size:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > player_size:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # Update bullet positions
    for bullet in bullets:
        bullet[0].y -= bullet_speed

    # Remove bullets that have left the screen
    bullets = [bullet for bullet in bullets if bullet[0].y > 0]

    # Create new enemies randomly
    if random.randint(1, 100) < 5:
        create_enemy()

    # Update enemy positions
    for enemy in enemies:
        enemy[0].y += enemy_speed

    # Check for collisions between bullets and enemies
    for bullet in bullets:
        for enemy in enemies:
            if bullet[0].colliderect(enemy[0]) and bullet[1] == enemy[1]:  # Check if bullet color matches enemy color
                bullets.remove(bullet)
                enemies.remove(enemy)
                # Add scoring here if desired

    # Check for collisions between player and enemies
    for enemy in enemies:
        if enemy[0].colliderect(pygame.Rect(player_x - player_size // 2, player_y - player_size, player_size, player_size)):
            player_lives -= 1
            enemies.remove(enemy)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the player (triangle)
    if player_lives > 0:
        pygame.draw.polygon(screen, WHITE, [(player_x, player_y - player_size),
                                             (player_x - player_size // 2, player_y + player_size),
                                             (player_x + player_size // 2, player_y + player_size)])
    else:
        # Player is destroyed
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, bullet[1], bullet[0])

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy[1], enemy[0])

    # Draw player lives
    font = pygame.font.Font(None, 24)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
