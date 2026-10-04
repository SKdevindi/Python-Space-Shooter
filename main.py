import pygame
import random
import os

# =====================================
# INITIALIZE
# =====================================

pygame.init()
pygame.mixer.init()

# =====================================
# GAME SETTINGS
# =====================================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()

# =====================================
# FONTS
# =====================================

small_font = pygame.font.Font(None, 28)
font = pygame.font.Font(None, 36)
medium_font = pygame.font.Font(None, 48)
big_font = pygame.font.Font(None, 75)

# =====================================
# COLORS
# =====================================

WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
DARK_BLUE = (5, 5, 25)
YELLOW = (255, 220, 50)
RED = (255, 60, 60)
GREEN = (80, 255, 120)

# =====================================
# IMAGE SETTINGS
# =====================================

PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70

ENEMY_WIDTH = 60
ENEMY_HEIGHT = 60

# =====================================
# LOAD IMAGES
# =====================================

player_image = pygame.image.load(
    "assets/player.png"
).convert_alpha()

enemy_image = pygame.image.load(
    "assets/enemy.png"
).convert_alpha()

player_image = pygame.transform.smoothscale(
    player_image,
    (PLAYER_WIDTH, PLAYER_HEIGHT)
)

enemy_image = pygame.transform.smoothscale(
    enemy_image,
    (ENEMY_WIDTH, ENEMY_HEIGHT)
)

# =====================================
# LOAD SOUND EFFECTS
# =====================================

shoot_sound = pygame.mixer.Sound(
    "assets/shoot.wav"
)

explosion_sound = pygame.mixer.Sound(
    "assets/explosion.wav"
)

shoot_sound.set_volume(0.35)
explosion_sound.set_volume(0.45)

# =====================================
# BACKGROUND MUSIC
# =====================================

pygame.mixer.music.load(
    "assets/background.wav"
)

pygame.mixer.music.set_volume(0.20)

# Repeat forever
pygame.mixer.music.play(-1)

# =====================================
# HIGH SCORE
# =====================================

HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():

    if os.path.exists(HIGH_SCORE_FILE):

        try:

            with open(
                HIGH_SCORE_FILE,
                "r"
            ) as file:

                return int(file.read())

        except ValueError:

            return 0

    return 0


def save_high_score(value):

    with open(
        HIGH_SCORE_FILE,
        "w"
    ) as file:

        file.write(
            str(value)
        )


high_score = load_high_score()

# =====================================
# STARS
# =====================================

stars = []

for i in range(120):

    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])

# =====================================
# PLAYER
# =====================================

player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT - 90

player_speed = 6

# =====================================
# BULLETS
# =====================================

bullets = []

BULLET_WIDTH = 6
BULLET_HEIGHT = 18

bullet_speed = 9

# =====================================
# CREATE ENEMIES
# =====================================


def create_enemies(number=5):

    new_enemies = []

    for i in range(number):

        new_enemies.append([
            random.randint(
                20,
                WIDTH - ENEMY_WIDTH - 20
            ),

            random.randint(
                -500,
                -60
            )
        ])

    return new_enemies


enemies = create_enemies(5)

# =====================================
# GAME VARIABLES
# =====================================

explosions = []

score = 0
lives = 3

level = 1
enemy_speed = 3

game_started = False
game_over = False
paused = False

music_on = True
sound_on = True

# =====================================
# RESTART GAME
# =====================================


def restart_game():

    global player_x
    global player_y

    global bullets
    global enemies
    global explosions

    global score
    global lives

    global level
    global enemy_speed

    global game_started
    global game_over
    global paused

    player_x = WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = HEIGHT - 90

    bullets = []
    explosions = []

    enemies = create_enemies(5)

    score = 0
    lives = 3

    level = 1
    enemy_speed = 3

    game_started = True
    game_over = False
    paused = False

# =====================================
# DRAW STARS
# =====================================


def draw_stars():

    for star in stars:

        pygame.draw.circle(
            screen,
            WHITE,
            (star[0], star[1]),
            star[2]
        )

# =====================================
# MAIN GAME LOOP
# =====================================


running = True

while running:

    # =================================
    # EVENTS
    # =================================

    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:

            save_high_score(high_score)

            running = False

        # Keyboard
        if event.type == pygame.KEYDOWN:

            # =================================
            # MUSIC ON / OFF
            # =================================

            if event.key == pygame.K_m:

                music_on = not music_on

                if music_on:

                    pygame.mixer.music.unpause()

                else:

                    pygame.mixer.music.pause()

            # =================================
            # SOUND EFFECTS ON / OFF
            # =================================

            if event.key == pygame.K_n:

                sound_on = not sound_on

            # =================================
            # MAIN MENU
            # =================================

            if not game_started:

                if event.key == pygame.K_RETURN:

                    restart_game()

            # =================================
            # GAME OVER
            # =================================

            elif game_over:

                # R = Restart
                if event.key == pygame.K_r:

                    restart_game()

                # ESC = Main Menu
                if event.key == pygame.K_ESCAPE:

                    game_started = False
                    game_over = False
                    paused = False

            # =================================
            # NORMAL GAME
            # =================================

            else:

                # P = Pause / Resume
                if event.key == pygame.K_p:

                    paused = not paused

                # ESC = Main Menu
                if event.key == pygame.K_ESCAPE:

                    game_started = False
                    paused = False

                # SPACE = Shoot
                if (
                    event.key == pygame.K_SPACE
                    and not paused
                ):

                    bullets.append([
                        player_x
                        + PLAYER_WIDTH // 2
                        - BULLET_WIDTH // 2,

                        player_y
                    ])

                    if sound_on:

                        shoot_sound.play()

    # =====================================
    # GAME LOGIC
    # =====================================

    if (
        game_started
        and not game_over
        and not paused
    ):

        # =================================
        # LEVEL SYSTEM
        # =================================

        new_level = (score // 10) + 1

        if new_level > level:

            level = new_level

            # Increase enemy speed
            enemy_speed = (
                3
                + (level - 1) * 0.7
            )

            # Add more enemies
            if len(enemies) < 10:

                enemies.append([
                    random.randint(
                        20,
                        WIDTH - ENEMY_WIDTH - 20
                    ),

                    random.randint(
                        -400,
                        -60
                    )
                ])

        # =================================
        # PLAYER MOVEMENT
        # =================================

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:

            player_x -= player_speed

        if keys[pygame.K_RIGHT]:

            player_x += player_speed

        # Keep player inside screen
        player_x = max(
            0,
            min(
                player_x,
                WIDTH - PLAYER_WIDTH
            )
        )

        # =================================
        # MOVE BULLETS
        # =================================

        for bullet in bullets[:]:

            bullet[1] -= bullet_speed

            if bullet[1] < -BULLET_HEIGHT:

                bullets.remove(bullet)

        # =================================
        # MOVE ENEMIES
        # =================================

        for enemy in enemies:

            enemy[1] += enemy_speed

            if enemy[1] > HEIGHT:

                enemy[0] = random.randint(
                    20,
                    WIDTH - ENEMY_WIDTH - 20
                )

                enemy[1] = random.randint(
                    -250,
                    -60
                )

        # =================================
        # BULLET / ENEMY COLLISION
        # =================================

        for bullet in bullets[:]:

            bullet_rect = pygame.Rect(
                bullet[0],
                bullet[1],
                BULLET_WIDTH,
                BULLET_HEIGHT
            )

            for enemy in enemies:

                enemy_rect = pygame.Rect(
                    enemy[0] + 8,
                    enemy[1] + 8,
                    ENEMY_WIDTH - 16,
                    ENEMY_HEIGHT - 16
                )

                if bullet_rect.colliderect(
                    enemy_rect
                ):

                    # Explosion animation
                    explosions.append([
                        int(
                            enemy[0]
                            + ENEMY_WIDTH / 2
                        ),

                        int(
                            enemy[1]
                            + ENEMY_HEIGHT / 2
                        ),

                        5
                    ])

                    # Explosion sound
                    if sound_on:

                        explosion_sound.play()

                    # Remove bullet
                    if bullet in bullets:

                        bullets.remove(bullet)

                    # Reset enemy
                    enemy[0] = random.randint(
                        20,
                        WIDTH - ENEMY_WIDTH - 20
                    )

                    enemy[1] = random.randint(
                        -250,
                        -60
                    )

                    # Score
                    score += 1

                    # High Score
                    if score > high_score:

                        high_score = score

                        save_high_score(
                            high_score
                        )

                    break

        # =================================
        # PLAYER / ENEMY COLLISION
        # =================================

        player_rect = pygame.Rect(
            player_x + 10,
            player_y + 10,
            PLAYER_WIDTH - 20,
            PLAYER_HEIGHT - 20
        )

        for enemy in enemies:

            enemy_rect = pygame.Rect(
                enemy[0] + 8,
                enemy[1] + 8,
                ENEMY_WIDTH - 16,
                ENEMY_HEIGHT - 16
            )

            if player_rect.colliderect(
                enemy_rect
            ):

                # Explosion
                explosions.append([
                    int(
                        enemy[0]
                        + ENEMY_WIDTH / 2
                    ),

                    int(
                        enemy[1]
                        + ENEMY_HEIGHT / 2
                    ),

                    5
                ])

                # Explosion sound
                if sound_on:

                    explosion_sound.play()

                # Lose life
                lives -= 1

                # Reset enemy
                enemy[0] = random.randint(
                    20,
                    WIDTH - ENEMY_WIDTH - 20
                )

                enemy[1] = random.randint(
                    -250,
                    -60
                )

                # Game Over
                if lives <= 0:

                    lives = 0
                    game_over = True

    # =====================================
    # UPDATE EXPLOSIONS
    # =====================================

    if not paused:

        for explosion in explosions[:]:

            explosion[2] += 2

            if explosion[2] > 40:

                explosions.remove(
                    explosion
                )

    # =====================================
    # BACKGROUND
    # =====================================

    screen.fill(DARK_BLUE)

    draw_stars()

    # =====================================
    # MAIN MENU
    # =====================================

    if not game_started:

        # Title
        title = big_font.render(
            "SPACE SHOOTER",
            True,
            BLUE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    WIDTH // 2,
                    100
                )
            )
        )

        # Subtitle
        subtitle = small_font.render(
            "Destroy the enemy fleet and survive!",
            True,
            WHITE
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(
                    WIDTH // 2,
                    155
                )
            )
        )

        # Player spaceship
        menu_player = pygame.transform.smoothscale(
            player_image,
            (100, 100)
        )

        screen.blit(
            menu_player,
            menu_player.get_rect(
                center=(
                    WIDTH // 2,
                    235
                )
            )
        )

        # Play
        play_text = medium_font.render(
            "PRESS ENTER TO PLAY",
            True,
            GREEN
        )

        screen.blit(
            play_text,
            play_text.get_rect(
                center=(
                    WIDTH // 2,
                    325
                )
            )
        )

        # Controls title
        controls_title = font.render(
            "CONTROLS",
            True,
            YELLOW
        )

        screen.blit(
            controls_title,
            controls_title.get_rect(
                center=(
                    WIDTH // 2,
                    385
                )
            )
        )

        controls = [
            "LEFT / RIGHT  -  Move",
            "SPACE  -  Shoot",
            "P  -  Pause / Resume",
            "M  -  Music ON / OFF",
            "N  -  Sound ON / OFF"
        ]

        y = 425

        for control in controls:

            control_text = small_font.render(
                control,
                True,
                WHITE
            )

            screen.blit(
                control_text,
                control_text.get_rect(
                    center=(
                        WIDTH // 2,
                        y
                    )
                )
            )

            y += 28

        # High Score
        high_text = small_font.render(
            f"High Score: {high_score}",
            True,
            BLUE
        )

        screen.blit(
            high_text,
            (
                20,
                20
            )
        )

    # =====================================
    # GAME SCREEN
    # =====================================

    else:

        # =================================
        # PLAYER
        # =================================

        if not game_over:

            screen.blit(
                player_image,
                (
                    player_x,
                    player_y
                )
            )

        # =================================
        # BULLETS
        # =================================

        for bullet in bullets:

            # Outer blue glow
            pygame.draw.rect(
                screen,
                (0, 100, 255),
                (
                    bullet[0] - 2,
                    bullet[1],
                    BULLET_WIDTH + 4,
                    BULLET_HEIGHT
                ),
                border_radius=3
            )

            # Bright center
            pygame.draw.rect(
                screen,
                (100, 230, 255),
                (
                    bullet[0],
                    bullet[1],
                    BULLET_WIDTH,
                    BULLET_HEIGHT
                ),
                border_radius=3
            )

        # =================================
        # ENEMIES
        # =================================

        if not game_over:

            for enemy in enemies:

                screen.blit(
                    enemy_image,
                    (
                        enemy[0],
                        enemy[1]
                    )
                )

        # =================================
        # EXPLOSIONS
        # =================================

        for explosion in explosions:

            x = explosion[0]
            y = explosion[1]
            size = explosion[2]

            # Outer
            pygame.draw.circle(
                screen,
                (255, 60, 0),
                (x, y),
                size
            )

            # Middle
            pygame.draw.circle(
                screen,
                (255, 150, 0),
                (x, y),
                max(
                    1,
                    size - 8
                )
            )

            # Center
            pygame.draw.circle(
                screen,
                (255, 255, 150),
                (x, y),
                max(
                    1,
                    size - 16
                )
            )

        # =================================
        # HUD
        # =================================

        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (
                20,
                20
            )
        )

        level_text = font.render(
            f"Level: {level}",
            True,
            YELLOW
        )

        screen.blit(
            level_text,
            level_text.get_rect(
                midtop=(
                    WIDTH // 2,
                    20
                )
            )
        )

        lives_text = font.render(
            f"Lives: {lives}",
            True,
            WHITE
        )

        screen.blit(
            lives_text,
            (
                WIDTH
                - lives_text.get_width()
                - 20,
                20
            )
        )

        high_text = small_font.render(
            f"High Score: {high_score}",
            True,
            BLUE
        )

        screen.blit(
            high_text,
            (
                20,
                60
            )
        )

        # Music Status
        music_status = (
            "ON"
            if music_on
            else "OFF"
        )

        music_text = small_font.render(
            f"Music: {music_status}",
            True,
            WHITE
        )

        screen.blit(
            music_text,
            (
                WIDTH
                - music_text.get_width()
                - 20,
                60
            )
        )

        # Sound Status
        sound_status = (
            "ON"
            if sound_on
            else "OFF"
        )

        sound_text = small_font.render(
            f"Sound: {sound_status}",
            True,
            WHITE
        )

        screen.blit(
            sound_text,
            (
                WIDTH
                - sound_text.get_width()
                - 20,
                90
            )
        )

        # =================================
        # PAUSE SCREEN
        # =================================

        if paused and not game_over:

            overlay = pygame.Surface(
                (
                    WIDTH,
                    HEIGHT
                )
            )

            overlay.set_alpha(180)

            overlay.fill(
                (0, 0, 0)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            paused_text = big_font.render(
                "PAUSED",
                True,
                BLUE
            )

            screen.blit(
                paused_text,
                paused_text.get_rect(
                    center=(
                        WIDTH // 2,
                        245
                    )
                )
            )

            resume_text = font.render(
                "Press P to Resume",
                True,
                WHITE
            )

            screen.blit(
                resume_text,
                resume_text.get_rect(
                    center=(
                        WIDTH // 2,
                        330
                    )
                )
            )

            menu_text = small_font.render(
                "Press ESC for Main Menu",
                True,
                YELLOW
            )

            screen.blit(
                menu_text,
                menu_text.get_rect(
                    center=(
                        WIDTH // 2,
                        380
                    )
                )
            )

        # =================================
        # GAME OVER
        # =================================

        if game_over:

            overlay = pygame.Surface(
                (
                    WIDTH,
                    HEIGHT
                )
            )

            overlay.set_alpha(180)

            overlay.fill(
                (0, 0, 0)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            game_over_text = big_font.render(
                "GAME OVER",
                True,
                RED
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(
                    center=(
                        WIDTH // 2,
                        175
                    )
                )
            )

            final_score_text = font.render(
                f"Final Score: {score}",
                True,
                YELLOW
            )

            screen.blit(
                final_score_text,
                final_score_text.get_rect(
                    center=(
                        WIDTH // 2,
                        270
                    )
                )
            )

            level_reached_text = font.render(
                f"Level Reached: {level}",
                True,
                WHITE
            )

            screen.blit(
                level_reached_text,
                level_reached_text.get_rect(
                    center=(
                        WIDTH // 2,
                        320
                    )
                )
            )

            high_score_text = font.render(
                f"High Score: {high_score}",
                True,
                BLUE
            )

            screen.blit(
                high_score_text,
                high_score_text.get_rect(
                    center=(
                        WIDTH // 2,
                        370
                    )
                )
            )

            restart_text = font.render(
                "Press R to Restart",
                True,
                GREEN
            )

            screen.blit(
                restart_text,
                restart_text.get_rect(
                    center=(
                        WIDTH // 2,
                        440
                    )
                )
            )

            menu_text = small_font.render(
                "Press ESC for Main Menu",
                True,
                WHITE
            )

            screen.blit(
                menu_text,
                menu_text.get_rect(
                    center=(
                        WIDTH // 2,
                        490
                    )
                )
            )

    # =====================================
    # UPDATE DISPLAY
    # =====================================

    pygame.display.update()

    clock.tick(60)


# =====================================
# CLOSE GAME
# =====================================

save_high_score(high_score)

pygame.quit()