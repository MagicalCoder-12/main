import pygame
import one_player
import two_player

# Initialize Pygame
pygame.font.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1200, 700
MENU_FONT = pygame.font.SysFont('comicsans', 40)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FPS = 60

# Pygame setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

# Initialize menu components
oneplayer_text = MENU_FONT.render("1 Player", 2, BLACK)
twoplayer_text = MENU_FONT.render("VS Mode", 2, BLACK)
oneplayer_rect = pygame.Rect(WIDTH // 2 - oneplayer_text.get_width() // 2, 150, oneplayer_text.get_width(), 70)
twoplayer_rect = pygame.Rect(WIDTH // 2 - twoplayer_text.get_width() // 2, 300, twoplayer_text.get_width(), 70)

# Game selection menu
def draw_menu():
    WIN.fill(GREEN)

    pygame.draw.rect(WIN, BLACK, oneplayer_rect, 4)
    pygame.draw.rect(WIN, BLACK, twoplayer_rect, 4)

    WIN.blit(oneplayer_text, (oneplayer_rect.x, oneplayer_rect.y))
    WIN.blit(twoplayer_text, (twoplayer_rect.x, twoplayer_rect.y))

    pygame.display.update()

# Function to handle one player mode
def run_oneplayer():
    # Call the main menu function of the one_player module
    one_player.main_menu()

# Function to handle two player mode
def run_twoplayer():
    # Call the run_space function of the two_player module with WIDTH and HEIGHT arguments
    two_player.run_space(WIDTH, HEIGHT)

# Main function for menu and game selection
def main():
    menu_running = True

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if oneplayer_rect.collidepoint(pos):
                    run_oneplayer()
                    menu_running = False
                elif twoplayer_rect.collidepoint(pos):
                    run_twoplayer()
                    menu_running = False

        draw_menu()

if __name__ == "__main__":
    main()