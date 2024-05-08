import pygame
import os
import random

# Define the PowerUp class
class PowerUp:
    def __init__(self, image_path, animation_steps, pos):
        self.image_list = []
        self.load_images(image_path, animation_steps)
        self.pos = pos
        self.frame = 0
        self.animation_cooldown = 75
        self.last_update = pygame.time.get_ticks()
        self.gravity = 0.1

    def load_images(self, image_path, animation_steps):
        image = pygame.image.load(image_path).convert_alpha()
        width, height = image.get_width() // animation_steps, image.get_height()
        for x in range(animation_steps):
            self.image_list.append(image.subsurface(x * width, 0, width, height))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.image_list):
                self.frame = 0
        self.pos[1] += self.gravity
        if self.pos[1] > SCREEN_HEIGHT:
            self.pos[1] = -32

    def draw(self, screen):
        screen.blit(self.image_list[self.frame], self.pos)

# Initialize Pygame
pygame.init()
FPS = 60
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
Gravity = 0.1

# Set up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Spritesheets')

# Load background
BG = (250, 250, 250)

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
    random_pos = [random.randint(0, SCREEN_WIDTH - 32), -32]
    random_powerup = PowerUp(random_powerup_image, 17, random_pos)
    powerups.append(random_powerup)

# Initial addition of a random power-up
add_random_powerup()

# Timer variables
last_powerup_time = pygame.time.get_ticks()
powerup_interval = 2000  # 2 seconds

run = True
while run:
    screen.fill(BG)

    # Update and draw each power-up in the list
    for powerup in powerups:
        powerup.update()
        powerup.draw(screen)

    # Check if it's time to add a new random power-up
    current_time = pygame.time.get_ticks()
    if current_time - last_powerup_time >= powerup_interval:
        add_random_powerup()
        last_powerup_time = current_time

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.size
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    pygame.display.update()

pygame.quit()
