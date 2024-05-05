import pygame
import os
import button  # Importing the Button class
import one_player
import two_player

# Initialize Pygame
pygame.font.init()
pygame.mixer.init()

# Music
pygame.mixer.music.load('D:\\programs\\pygame\\Space\\Assets\\Sounds\\CHAMPION.ogg')
pygame.mixer.music.set_volume(1.0) 
start_music = pygame.mixer.Sound('D:\\programs\\pygame\\Space\\Assets\\Sounds\\game_start.wav')

# Constants
MENU_FONT = pygame.font.SysFont('comicsans', 40)
WHITE = (255,255,255)
FPS = 60
BG = pygame.transform.scale(pygame.image.load(os.path.join(r'D:\programs\pygame\Space\Assets\Background\background-black.png')), (1360, 768))

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Space Battle")

# Initialize menu components
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()
start_img = pygame.image.load('images/start.png').convert_alpha()

# Create button instances
start_button = button.Button(600, 220, start_img, 1)
options_button = button.Button(570, 340, options_img, 1)
quit_button = button.Button(600, 455, quit_img, 1)
resume_button = button.Button(304, 125, resume_img, 1)
video_button = button.Button(226, 75, video_img, 1)
audio_button = button.Button(225, 200, audio_img, 1)
keys_button = button.Button(246, 325, keys_img, 1)
back_button = button.Button(600, 450, back_img, 1)


oneplayer_text = MENU_FONT.render("1 Player", 2, WHITE)
twoplayer_text = MENU_FONT.render("VS Mode", 2, WHITE)
oneplayer_rect = pygame.Rect(WIDTH // 2 - oneplayer_text.get_width() // 2, 150, oneplayer_text.get_width(), 70)
twoplayer_rect = pygame.Rect(WIDTH // 2 - twoplayer_text.get_width() // 2, 300, twoplayer_text.get_width(), 70)

# Game selection menu
def draw_menu():
    screen.blit(BG, (0, 0))

    # Draw buttons on screen
    start_button.draw(screen)
    options_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.update()

# Function to handle one player mode
def run_oneplayer():
    # Call the main menu function of the one_player module
    one_player.main_menu()

# Function to handle two player mode
def run_twoplayer():
    # Call the run_space function of the two_player module with WIDTH and HEIGHT arguments
    two_player.run_space()

# Placeholder functions for button actions
def start_action():
    start_music.play()
    screen.blit(BG, (0, 0))

    pygame.draw.rect(screen, WHITE, oneplayer_rect, 4)
    pygame.draw.rect(screen, WHITE, twoplayer_rect, 4)

    screen.blit(oneplayer_text, (oneplayer_rect.x, oneplayer_rect.y))
    screen.blit(twoplayer_text, (twoplayer_rect.x, twoplayer_rect.y))

    back_button.draw(screen)  # Draw the back button
    pygame.display.update()

    back_clicked = False
    while not back_clicked:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if oneplayer_rect.collidepoint(pos):
                    run_oneplayer()  # Call run_oneplayer function when "1 Player" is clicked
                    back_clicked = True
                    break
                elif twoplayer_rect.collidepoint(pos):
                    run_twoplayer()  # Call run_twoplayer function when "VS Mode" is clicked
                    back_clicked = True
                    break
                elif back_button.rect.collidepoint(pos):
                    back_clicked = True
                    break

menu_state = "main"  # Initialize menu state outside of the function

def options_action():
    global menu_state  # Add global declaration to modify the menu_state variable

    if options_button.draw(screen):
        menu_state = "options"

    if menu_state == "options":
        #draw the different options buttons
        if video_button.draw(screen):
            print("Video Settings")
        if audio_button.draw(screen):
            print("Audio Settings")
        if keys_button.draw(screen):
            print("Change Key Bindings")
        if back_button.draw(screen):
            menu_state = "main"


def quit_action():
    pygame.quit()
    quit()

# Main function for menu and game selection
def main():
    menu_running = True

    pygame.mixer.music.play(-1)  # Play the play_music continuously

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.rect.collidepoint(pos):
                    # Handle start button action
                    start_action()
                elif options_button.rect.collidepoint(pos):
                    # Handle options button action
                    options_action()
                elif quit_button.rect.collidepoint(pos):
                    # Handle quit button action
                    quit_action()
                    menu_running = False

        draw_menu()

if __name__ == "__main__":
    main()
