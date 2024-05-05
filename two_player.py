import pygame
import os


pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set display mode to fullscreen
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("Space Battle")

BORDER = pygame.Rect(WIN.get_width() // 2 - 5, 0, 10, WIN.get_height())
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('D:\\programs\\pygame\\Space\\Assets\\Sounds\\Grenade-1.ogg'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('D:\\programs\\pygame\\Space\\Assets\\Sounds\\Gun-Silencer.ogg'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 4
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 50

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(r'D:\programs\pygame\Space\main\Assets\spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(r'D:\programs\pygame\Space\main\Assets\spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join(r'D:\programs\pygame\Space\main\Assets\Background\space.png')), (WIN.get_width(), WIN.get_height()))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    global WIN, SPACE, BORDER
    WIN.blit(SPACE, (0, 0))

    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIN.get_width() - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < WIN.get_height() - 15:
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIN.get_width():
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < WIN.get_height() - 15:
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIN.get_width():  # Check if the bullet is out of the window
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:  # Check if the bullet is out of the window
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIN.get_width() // 2 - draw_text.get_width() // 2, WIN.get_height() // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def run_space():
    global WIN, BORDER, SPACE
    red = pygame.Rect(1200, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10

    pygame.mixer.music.load(r'D:\programs\pygame\Space\main\Assets\Sounds\music2.wav')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)

    start_music = pygame.mixer.Sound(r'D:\programs\pygame\Space\main\Assets\Sounds\game_start.wav')
    start_music.set_volume(1.0)
    start_music.play()

    clock = pygame.time.Clock()
    run_game = True

    while run_game:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle quitting the game
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_l and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    run_space()
