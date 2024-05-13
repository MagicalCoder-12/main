import pygame
import os
import random
import sys

pygame.init()
pygame.mixer.init()

# Get the screen dimensions
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

# Set up the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Shooter")

# Load background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Background", "Universe.png")), (WIDTH, HEIGHT))

# Load spaceship sprite sheets
SPACESHIP_BLUE_SHEET = pygame.image.load(os.path.join("Assets", "MainCharacters", "Spaceships", "spaceship_blue_spritesheet.png"))
SPACESHIP_RED_SHEET = pygame.image.load(os.path.join("Assets", "MainCharacters", "Spaceships", "spaceship_red_spritesheet.png"))
SPACESHIP_SHADOW_SHEET = pygame.image.load(os.path.join("Assets", "MainCharacters", "Spaceships", "spaceship_shadow_spritesheet.png"))

RED_SPACE_SHIP = pygame.image.load(os.path.join("Assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("Assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("Assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("Assets", "pixel_ship_yellow.png"))
YELLOW_ENEMY_SHIP = pygame.transform.rotate(YELLOW_SPACE_SHIP, 180)

# Load the original image
original_image = pygame.image.load(os.path.join("Assets", "alien.png"))

# Get the original width and height
original_width = original_image.get_width()
original_height = original_image.get_height()

# Calculate the desired width and height for resizing
desired_width = original_width * 3
desired_height = original_height * 3

# Resize the image
PURPLE_ENEMY_SHIP = pygame.transform.scale(original_image, (desired_width, desired_height))
PURPLE_ENEMY_SHIP.set_colorkey((255, 255, 255))

# Load collectibles sprite sheets
APPLE_SHEET = pygame.image.load(os.path.join("Assets", "Items", "Fruits", "Apple.png"))
BANANA_SHEET = pygame.image.load(os.path.join("Assets", "Items", "Fruits", "Bananas.png"))
STRAWBERRY_SHEET = pygame.image.load(os.path.join("Assets", "Items", "Fruits", "Strawberry.png"))

# Load collected effect sprite sheet
COLLECTED_EFFECT_SHEET = pygame.image.load(os.path.join("Assets", "Items", "Fruits", "Collected.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_yellow.png"))
PURPLE_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_purple.png")).convert()
PURPLE_LASER.set_colorkey((0, 0, 0))

# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Grenade-1.ogg"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "shoot.mp3"))
BULLET_FIRE_SOUND.set_volume(0.4)

# Define the number of rows and columns in the sprite sheet
ROWS = 1
COLS = 5

# Calculate the width and height of each frame
FRAME_WIDTH = SPACESHIP_BLUE_SHEET.get_width() // COLS
FRAME_HEIGHT = SPACESHIP_BLUE_SHEET.get_height() // ROWS

# Create lists to store individual frames for each spaceship
SPACESHIP_BLUE_FRAMES = []
SPACESHIP_RED_FRAMES = []
SPACESHIP_SHADOW_FRAMES = []

# Extract frames from the sprite sheets
for row in range(ROWS):
    for col in range(COLS):
        frame_blue = pygame.transform.scale(SPACESHIP_BLUE_SHEET.subsurface(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT), (FRAME_WIDTH * 3, FRAME_HEIGHT * 3))
        frame_red = pygame.transform.scale(SPACESHIP_RED_SHEET.subsurface(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT), (FRAME_WIDTH * 3, FRAME_HEIGHT * 3))
        frame_shadow = pygame.transform.scale(SPACESHIP_SHADOW_SHEET.subsurface(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT), (FRAME_WIDTH * 3, FRAME_HEIGHT * 3))
        SPACESHIP_BLUE_FRAMES.append(frame_blue)
        SPACESHIP_RED_FRAMES.append(frame_red)
        SPACESHIP_SHADOW_FRAMES.append(frame_shadow)


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 10

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.bullet_fire_sound = BULLET_FIRE_SOUND
        self.last_shot_time = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.COOLDOWN:
            # Play the shooting sound
            self.bullet_fire_sound.play()
            # Create the laser object
            laser = Laser(self.x + self.ship_img.get_width() // 2 - self.laser_img.get_width() // 2, self.y, self.laser_img)
            self.lasers.append(laser)
            # Update the time of the last shot
            self.last_shot_time = current_time

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()



class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.vel = 5
        self.frames = SPACESHIP_BLUE_FRAMES
        self.frame_index = 0
        self.animation_speed = 0.2 # Increase this value to slow down the animation even further
        self.frame_count = 0
        self.img = self.frames[self.frame_index]
        self.mask = pygame.mask.from_surface(self.img)
        self.laser_img = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
        self.max_health = health 
        self.health = health  # Set both health and max_health initially
        self.lasers = []
        self.cooldown_counter = 0
        self.shoot_cooldown = 0  # Add a new attribute for shoot cooldown
        self.invincible_start_time = 0  # Add attribute for invincibility start time
        self.continuous_shoot_start_time = 0  # Add attribute for continuous shooting start time

    def draw(self, window):
        # Update frame count
        self.frame_count += 1
        # Check if it's time to change frames
        if self.frame_count >=        10:  # Increase this value to slow down the animation even further
            self.frame_count = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)  # Cycle through frames
        self.img = self.frames[self.frame_index]
        self.healthbar(window)
        window.blit(self.img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x - self.vel > 0:  # Move left
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.get_width() < WIDTH:  # Move right
            self.x += self.vel
        if keys[pygame.K_UP] and self.y - self.vel > 0:  # Move up
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y + self.vel + self.get_height() + 15 < HEIGHT:  # Move down (+15 for extra space below)
            self.y += self.vel

    def shoot(self):
        # Adjust laser starting position
        if self.shoot_cooldown == 0:
            laser = Laser(self.x + self.img.get_width() // 2 - self.laser_img.get_width() // 2, self.y, self.laser_img)
            self.lasers.append(laser)
            # Reset shoot cooldown
            self.shoot_cooldown = 30  # Set the cooldown period (adjust as needed)

    def move_lasers(self, vel, objs):
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))
        green_width = self.img.get_width() * (self.health / self.max_health)
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.img.get_height() + 10, green_width, 10))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER, 10),    # Assign score values for each enemy type
        "green": (GREEN_SPACE_SHIP, GREEN_LASER, 20),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER, 30),
        "yellow": (YELLOW_ENEMY_SHIP, YELLOW_LASER, 40)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img, self.score = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class PowerUp:
    def __init__(self, x, y, power_up_type):
        self.x = x
        self.y = y
        self.power_up_type = power_up_type
        if self.power_up_type == "apple":
            self.img = APPLE_SHEET
        elif self.power_up_type == "banana":
            self.img = BANANA_SHEET
        elif self.power_up_type == "strawberry":
            self.img = STRAWBERRY_SHEET
        self.mask = pygame.mask.from_surface(self.img)
        self.collected = False
        self.collected_time = pygame.time.get_ticks()  # Time when the power-up was collected

    def draw(self, window):
        if not self.collected:
            window.blit(self.img, (self.x, self.y))

    def update(self):
        self.y += 2  # Adjust the speed of the power-up falling

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    score=0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    power_ups = []  # Create an empty list to store power-ups
    wave_length = 5
    enemy_vel = 1

    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    # Hide the system cursor
    pygame.mouse.set_visible(False)

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))

        WIN.blit(score_label, (10, 50))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        # Draw lasers
        for laser in player.lasers:
            laser.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    # Main game loop
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, 100), random.choice(["red", "blue", "green", "yellow"]))
                enemies.append(enemy)

        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Quit the game when the 'X' button is clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x - player.get_width() / 2 > 0:  # Check if moving left will keep the ship within the left boundary
            if mouse_x + player.get_width() / 2 < WIDTH:  # Check if moving right will keep the ship within the right boundary
                player.x = mouse_x - player.get_width() / 2

        if mouse_y - player.get_height() / 2 > 0:  # Check if moving up will keep the ship within the top boundary
            if mouse_y + player.get_height() / 2 < HEIGHT:  # Check if moving down will keep the ship within the bottom boundary
                player.y = mouse_y - player.get_height() / 2

        # Shooting logic for continuous shooting while space key is held down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()
        # Shooting logic for continuous shooting while mouse button is held down
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            player.shoot()
            BULLET_FIRE_SOUND.play()
        # Player movement
        player.move()

       
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
 

            if enemy.health <= 0:
                print("Enemy destroyed!")
                score += enemy.score  # Increment score based on enemy type
                print("Current score:", score)
                enemies.remove(enemy)

            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                BULLET_HIT_SOUND.play()
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
               
        player.move_lasers(-laser_vel, enemies)

        for power_up in power_ups:
            power_up.update()

        # Check for collision between player and power-ups
        for power_up in power_ups[:]:
            if power_up.collision(player):
                if power_up.power_up_type == "apple":
                    lives += 5
                elif power_up.power_up_type == "banana":
                    player.invincible_start_time = pygame.time.get_ticks()  # Start timer for invincibility
                elif power_up.power_up_type == "strawberry":
                    player.continuous_shoot_start_time = pygame.time.get_ticks()  # Start timer for continuous shooting
                power_ups.remove(power_up)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press any key to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


if __name__ == "__main__":
    main_menu()
