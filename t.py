import pygame
import os
import random

# Initialize Pygame
pygame.init()
FPS = 60
WIDTH = 900
HEIGHT = 700
Gravity = 0.5

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Spritesheets')

# Load background
BG = (250, 250, 250)

SPACESHIP_RED_SHEET = pygame.image.load(os.path.join("Assets", "MainCharacters", "Spaceships", "spaceship_red_spritesheet.png"))
ASTROID = pygame.image.load(os.path.join("Assets", "Other", "asteroid_large_1.png"))

# Define the number of rows and columns in the sprite sheet
ROWS = 1
COLS = 5

# Calculate the width and height of each frame
FRAME_WIDTH = SPACESHIP_RED_SHEET.get_width() // COLS
FRAME_HEIGHT = SPACESHIP_RED_SHEET.get_height() // ROWS

# Create lists to store individual frames for each spaceship
SPACESHIP_RED_FRAMES = []
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Grenade-1.ogg"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "player_shoot.wav"))
BULLET_FIRE_SOUND.set_volume(0.4)

for row in range(ROWS):
    for col in range(COLS):
        frame_red = pygame.transform.scale(SPACESHIP_RED_SHEET.subsurface(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT), (FRAME_WIDTH * 3, FRAME_HEIGHT * 3))
        SPACESHIP_RED_FRAMES.append(frame_red)

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
        self.frames = SPACESHIP_RED_FRAMES
        self.frame_index = 0
        self.animation_speed = 0.2 # Increase this value to slow down the animation even further
        self.frame_count = 0
        self.img = self.frames[self.frame_index]
        self.mask = pygame.mask.from_surface(self.img)
        self.laser_img = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
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
        if self.frame_count >= 10:  # Increase this value to slow down the animation even further
            self.frame_count = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)  # Cycle through frames
        self.img = self.frames[self.frame_index]
        self.healthbar(window)
        window.blit(self.img, (self.x, self.y))

    def move(self):
        global WIDTH, HEIGHT
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

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
        if self.shoot_cooldown == 0 and (pygame.time.get_ticks() - self.continuous_shoot_start_time <= 10000 or self.continuous_shoot_start_time == 0):
            laser = Laser(self.x + self.img.get_width() // 2 - self.laser_img.get_width() // 2, self.y, self.laser_img)
            self.lasers.append(laser)
            # Reset shoot cooldown
            self.shoot_cooldown = 20  # Set the cooldown period (adjust as needed)


    def move_lasers(self, vel, objs):
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if pygame.time.get_ticks() - self.invincible_start_time <= 10000 or self.invincible_start_time == 0:
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


# Define the PowerUp class
class PowerUp:
    def __init__(self, image_path, animation_steps, pos, scale_factor=2):
        self.image_list = []
        self.load_images(image_path, animation_steps, scale_factor)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.animation_cooldown = 75
        self.last_update = pygame.time.get_ticks()
        self.gravity = 1.0
        self.mask = pygame.mask.from_surface(self.image_list[self.frame])
        self.type = self.get_type_from_image_path(image_path)

    def load_images(self, image_path, animation_steps, scale_factor):
        image = pygame.image.load(image_path).convert_alpha()
        width, height = image.get_width() // animation_steps, image.get_height()
        for x in range(animation_steps):
            scaled_image = pygame.transform.scale(image.subsurface(x * width, 0, width, height), (width * scale_factor, height * scale_factor))
            self.image_list.append(scaled_image)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.image_list):
                self.frame = 0
            self.mask = pygame.mask.from_surface(self.image_list[self.frame])
        self.pos[1] += self.gravity
        self.y = self.pos[1]
        if self.pos[1] > HEIGHT:
            self.pos[1] = -32
            self.y = self.pos[1]

    def draw(self, screen):
        screen.blit(self.image_list[self.frame], self.pos)

    def get_type_from_image_path(self, image_path):
        filename = os.path.basename(image_path)
        if "Apple" in filename:
            return "Apple"
        elif "Bananas" in filename:
            return "Banana"
        elif "Strawberry" in filename:
            return "Strawberry"
        else:
            return "Unknown"


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

# Create instances of PowerUp class
powerup_images = [
    os.path.join(r'D:\programs\pygame\Assets\Items\Fruits\Apple.png'),
    os.path.join(r'D:\programs\pygame\Assets\Items\Fruits\Bananas.png'),
    os.path.join(r'D:\programs\pygame\Assets\Items\Fruits\Strawberry.png')
]

# Create an empty list to store PowerUp instances
powerups = []

# Function to randomly choose a power-up and add it to the list
def add_random_powerup():
    random_powerup_image = random.choice(powerup_images)
    random_pos = [random.randint(0, WIDTH - 32), -32]
    random_powerup = PowerUp(random_powerup_image, 17, random_pos)
    powerups.append(random_powerup)

# Initial addition of a random power-up
add_random_powerup()

# Timer variables
last_powerup_time = pygame.time.get_ticks()
# Define the range for random power-up interval
min_powerup_interval = 20000  # 20 seconds (in milliseconds)
max_powerup_interval = 60000  # 60 seconds (in milliseconds)

# Randomly select the power-up interval within the defined range
powerup_interval = random.randint(min_powerup_interval, max_powerup_interval)

# Asteroid variables
ASTEROID_WIDTH = 29
ASTEROID_HEIGHT = 29
ASTROID_SCALE_FACTOR = 2
ASTROID = pygame.transform.scale(ASTROID, (ASTROID.get_width() * ASTROID_SCALE_FACTOR, ASTROID.get_height() * ASTROID_SCALE_FACTOR))
asteroid_x = random.randint(0, WIDTH - ASTEROID_WIDTH)  # Randomize asteroid's initial x position
asteroid_y = -ASTEROID_HEIGHT  # Start asteroid above the screen
asteroid_vel = 1  # Set asteroid velocity
asteroids = []
def create_asteroid():
    asteroid_x = random.randint(0, WIDTH - ASTEROID_WIDTH)  # Randomize asteroid's initial x position
    asteroid_y = -ASTEROID_HEIGHT  # Start asteroid above the screen
    asteroid = {'x': asteroid_x, 'y': asteroid_y}
    asteroids.append(asteroid)

# Create initial asteroids
for _ in range(0,5):  # Create 5 initial asteroids
    create_asteroid()

def draw_asteroids(screen):
    for asteroid in asteroids:
        screen.blit(ASTROID, (asteroid['x'], asteroid['y']))

def move_asteroids():
    global asteroids
    asteroids = [asteroid for asteroid in asteroids if asteroid['y'] < HEIGHT]  # Remove off-screen asteroids
    for asteroid in asteroids:
        asteroid['y'] += asteroid_vel  # Move asteroid downwards
    if len(asteroids) < 5:  # Add new asteroids if there are fewer than 5 on screen
        create_asteroid()

def check_collision_player_asteroid(player, asteroid_x, asteroid_y):
    asteroid_mask = pygame.mask.from_surface(ASTROID)
    player_mask = pygame.mask.from_surface(player.img)
    offset = (int(asteroid_x - player.x), int(asteroid_y - player.y))
    collision_point = player_mask.overlap(asteroid_mask, offset)
    return collision_point is not None

def check_collision_lasers_asteroid(lasers, asteroid_x, asteroid_y):
    asteroid_mask = pygame.mask.from_surface(ASTROID)
    for laser in lasers:
        laser_mask = pygame.mask.from_surface(laser.img)
        offset = (int(asteroid_x - laser.x), int(asteroid_y - laser.y))
        collision_point = laser_mask.overlap(asteroid_mask, offset)
        if collision_point is not None:
            return True
    return False

def main():
    clock = pygame.time.Clock()
    global last_powerup_time  

    # Create a player object
    player = Player(WIDTH // 2, HEIGHT - 100)
    
    # Variables for scoring
    score = 0
    double_bonus = 0
    pygame.mixer.music.load(os.path.join('Assets', 'Sounds', 'music2.wav'))
    pygame.mixer.music.set_volume(0.6)
    #pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(False)
    
    # Main loop
    running = True
    while running:
        screen.fill(BG)  # Fill the screen with background color

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

        # Move the player
        player.move()

        # Draw the player
        player.draw(screen)


        # Draw and update lasers
        for laser in player.lasers:
            laser.draw(screen)
            laser.move(-2)  # Adjust the velocity as needed

        # Update and remove off-screen lasers
        player.move_lasers(-5, [])

        # Randomly add power-ups
        current_time = pygame.time.get_ticks()
        if current_time - last_powerup_time >= powerup_interval:
            random_powerup_image = random.choice(powerup_images)
            random_pos = [random.randint(0, WIDTH - 32), -32]
            random_powerup = PowerUp(random_powerup_image, 17, random_pos, scale_factor=2)  # Increase the scale_factor to 3
            powerups.append(random_powerup)
            last_powerup_time = current_time


        # Check for collisions with power-ups
        for powerup in powerups:
            if collide(player, powerup):
                powerups.remove(powerup)
                # Check the type of the collided power-up
                if powerup.type == "Apple" and player.health<100:
                    if pygame.time.get_ticks() > double_bonus:
                        player.health += 10 
                    else:
                        player.health += 20  # Double the health restoration if under double bonus effect
                elif powerup.type == "Banana":
                    double_bonus = pygame.time.get_ticks() + 10000  # Set the end time for doubling score
                elif powerup.type == "Strawberry":

                    # Activate invincibility for 10 seconds
                    player.invincible_start_time = pygame.time.get_ticks()+10000

        # Display score
        font = pygame.font.SysFont(None, 36)
        if pygame.time.get_ticks() <= double_bonus:
            text = font.render(f'Score: {score * 2}', True, (0, 0, 0))  # Double the score if the duration is still active
        else:
            text = font.render(f'Score: {score}', True, (0, 0, 0))

        screen.blit(text, (10, 10))
         # Display timer counter for banana power-up
        if pygame.time.get_ticks() <= double_bonus:
            remaining_time = (double_bonus - pygame.time.get_ticks()) // 1000  # Convert milliseconds to seconds
            timer_text = font.render(f'Double Bonus: {remaining_time}s', True, (0, 0, 0))
            screen.blit(timer_text, (10, 50))
        # Display timer counter for invincibility time
        if pygame.time.get_ticks() <= player.invincible_start_time:
            remaining_time = (player.invincible_start_time - pygame.time.get_ticks()) // 1000  # Convert milliseconds to seconds
            text_width, _ = font.size(f'Invincible time: {remaining_time}s')  # Get the width of the text
            text_x = WIDTH - text_width - 10  # Calculate the x-coordinate to position the text at the right corner with a margin of 10 pixels
            timer_text = font.render(f'Invincible time: {remaining_time}s', True, (0, 0, 0))
            screen.blit(timer_text, (text_x, 50))  # Position the text

        # Draw and move the asteroids
        draw_asteroids(screen)
        move_asteroids()
        
        # Check collisions between player and asteroids
        for asteroid in asteroids:
            if check_collision_player_asteroid(player, asteroid['x'], asteroid['y']):
                if pygame.time.get_ticks() - player.invincible_start_time >= 1000 or player.invincible_start_time == 0:
                    player.health -= 10  # Decrement player health by 10
                    score += 10
                asteroids.remove(asteroid)  # Remove the collided asteroid
                # Create a power-up at the asteroid's position
                new_powerup_pos = [asteroid['x'], asteroid['y']]
                random_powerup_image = random.choice(powerup_images)
                new_powerup = PowerUp(random_powerup_image, 17, new_powerup_pos, scale_factor=2)
                powerups.append(new_powerup)

        # Check collisions between lasers and asteroids
        lasers_to_remove = []  # Create a list to store lasers that need to be removed
        for laser in player.lasers:
            for asteroid in asteroids:
                if check_collision_lasers_asteroid([laser], asteroid['x'], asteroid['y']):
                    new_powerup_pos = [asteroid['x'], asteroid['y']]
                    random_powerup_image = random.choice(powerup_images)
                    new_powerup = PowerUp(random_powerup_image, 17, new_powerup_pos, scale_factor=2)
                    powerups.append(new_powerup)
                    lasers_to_remove.append(laser)  # Add the laser to the removal list
                    asteroids.remove(asteroid)  # Remove the collided asteroid
                    break  # Break out of the inner loop after collision detection

        # Remove lasers that collided with asteroids
        for laser in lasers_to_remove:
            player.lasers.remove(laser)



        # Draw and update power-ups
        for powerup in powerups:
            # Check if power-up is collected by colliding with the player or an asteroid
            collected = False
            if collide(player, powerup):
                collected = True
            for asteroid in asteroids:
                if check_collision_lasers_asteroid(player.lasers, asteroid['x'], asteroid['y']):
                    collected = True
                    break
            if not collected:
                powerup.update()
                powerup.draw(screen)

        # Check if player's health is zero or less
        if player.health <= 0:
            print("Game Over")
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()