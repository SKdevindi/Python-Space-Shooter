import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Player
player_x = 375
player_y = 520
player_speed = 6

# Bullets
bullets = []
bullet_speed = 8

# Enemies
enemies = []
enemy_speed = 3

# Score
score = 0

# Create enemies
for i in range(5):
    enemies.append([
        random.randint(20, WIDTH - 60),
        random.randint(-300, -40)
    ])

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot with SPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + 22, player_y])

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(player_x, WIDTH - 50))

    # Move bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed

        if bullet[1] < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy_speed

        if enemy[1] > HEIGHT:
            enemy[0] = random.randint(20, WIDTH - 60)
            enemy[1] = random.randint(-200, -40)

    # Collision
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(
            bullet[0], bullet[1], 6, 15
        )

        for enemy in enemies:
            enemy_rect = pygame.Rect(
                enemy[0], enemy[1], 40, 40
            )

            if bullet_rect.colliderect(enemy_rect):

                if bullet in bullets:
                    bullets.remove(bullet)

                enemy[0] = random.randint(20, WIDTH - 60)
                enemy[1] = random.randint(-200, -40)

                score += 1
                break

    # Background
    screen.fill((10, 10, 30))

    # Player spaceship
    pygame.draw.polygon(
        screen,
        (0, 200, 255),
        [
            (player_x + 25, player_y),
            (player_x, player_y + 50),
            (player_x + 25, player_y + 40),
            (player_x + 50, player_y + 50)
        ]
    )

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (bullet[0], bullet[1], 6, 15)
        )

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(
            screen,
            (255, 50, 50),
            (enemy[0], enemy[1], 40, 40)
        )

    # Score
    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (20, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()