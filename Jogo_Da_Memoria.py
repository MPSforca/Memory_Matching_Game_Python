import pygame
import os.path
import sys
import random
import ctypes

# Element at 0: Card back
IMAGES_NAME = ["costas", "carta1", "carta2", "carta3",
               "carta4", "carta5", "carta6", "carta7",
               "carta8"]

IMAGES_EXTENSION = ".png"

# Window Data
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

# Card data
CARD_WIDTH = 105
CARD_HEIGHT = 155

# List with every image loaded from the images_name
image_back = None

# Position of every card
cards_positions = []

# Board that the player is seeing
shown_board = []

# Board that represents every card flipped
actual_board = []

# Game data:
first_flipped_card_index = None
second_flipped_card_index = None
is_wrong = False
last_wrong_time = 0
how_many_pairs = 0

# Menu
MENU_WIDTH = 250
MENU_HEIGHT = WINDOW_HEIGHT

score = 0
match_time = 0
match_start_time = None
match_is_running = True
leave_button = None
restart_button = None
logo = None

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jogo da Memória")
pygame.display.set_icon(pygame.image.load(os.path.join("images", IMAGES_NAME[0] + IMAGES_EXTENSION)))

# Screen size and color
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen.fill((255, 255, 255))

# Load the logo:
logo = pygame.image.load(os.path.join("images", "logo.png"))
logo = pygame.transform.scale(logo, (250, 100))

# Load the images:
for image in IMAGES_NAME:
    card = pygame.image.load(os.path.join("images", image + IMAGES_EXTENSION))

    # Set image resolution:
    card = pygame.transform.scale(card, (CARD_WIDTH, CARD_HEIGHT))

    # It's not the first image (Card's back)
    if image_back is not None:
        # Adds twice => Two cards of each on board
        actual_board.append(card)
        actual_board.append(card)
    else:
        image_back = card


def draw_menu():
    # Reset:
    menu_rect = pygame.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect)

    # Logo:
    rect = pygame.Rect(0, 0, MENU_WIDTH, 100)
    screen.blit(logo, rect)
    write_game_data()

    # Line:
    pygame.draw.line(screen, (0, 0, 0), (MENU_WIDTH + 10, 0), (MENU_WIDTH + 10, MENU_HEIGHT))

    # Buttons to leave and restart:
    f = pygame.font.Font(os.path.join("fonts", "Montserrat-Regular.ttf"), 20)
    button_text = f.render("Reiniciar", 1, (0, 0, 0))
    global restart_button
    restart_button = screen.blit(button_text, (20, 600))

    button_text = f.render("Sair", 1, (0, 0, 0))
    global leave_button
    leave_button = screen.blit(button_text, (20, 630))


def start_match():
    # Shuffle the board
    random.shuffle(actual_board)

    global shown_board
    shown_board = [image_back] * 16

    draw_menu()

    # Updates the board that is being shown for the player
    create_board()

    # Reset variables:
    global score
    score = 0

    global match_start_time
    match_start_time = pygame.time.get_ticks()

    global first_flipped_card_index, second_flipped_card_index, is_wrong
    first_flipped_card_index = None
    second_flipped_card_index = None
    is_wrong = False

    global last_wrong_time, how_many_pairs, match_time, match_is_running
    last_wrong_time = 0
    how_many_pairs = 0
    match_time = 0
    match_is_running = True


# To write game pontuation and time
def write_game_data():

    f = pygame.font.Font(os.path.join("fonts", "Montserrat-Regular.ttf"), 20)
    text = f.render("Pontuação: " + str(score), 1, (0, 0, 0))
    screen.blit(text, (20, 150, 30, 210))

    text = f.render("Tempo: " + str(match_time) + "s", 1, (0, 0, 0))
    screen.blit(text, (20, 180, 30, 210))


def create_board():
    # Fill the board with images
    for i in range(0, 16):

        # Card position:
        x = 300 + CARD_WIDTH * (i % 4) + 40 * (i % 4)
        y = 20 + CARD_HEIGHT * (i // 4) + 20 * (i // 4)

        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        global cards_positions
        cards_positions.append(rect)

        screen.blit(image_back, rect)


def click_handler(mouse_x, mouse_y):
    if leave_button.collidepoint(mouse_x, mouse_y):
        sys.exit()
    elif restart_button.collidepoint(mouse_x, mouse_y):
        start_match()
    else:
        for i in range(0, 16):
            if cards_positions[i].collidepoint(mouse_x, mouse_y) and shown_board[i] == image_back:
                pygame.mixer.stop()
                pygame.mixer.Sound(os.path.join("sounds", "flip.wav")).play()
                shown_board[i] = actual_board[i]
                # Draws the card:
                screen.blit(shown_board[i], cards_positions[i])
                pygame.display.flip()
                global first_flipped_card_index
                # There's already a card facing front:
                if first_flipped_card_index is not None:
                    global second_flipped_card_index
                    second_flipped_card_index = i
                    # Wrong pair:
                    if (actual_board[first_flipped_card_index] != actual_board[second_flipped_card_index]):
                        global is_wrong, last_wrong_time, score
                        last_wrong_time = pygame.time.get_ticks()
                        is_wrong = True
                        score -= 1
                    else:
                        pygame.mixer.stop()
                        pygame.mixer.Sound(os.path.join("sounds", "point.wav")).play()
                        first_flipped_card_index = None
                        second_flipped_card_index = None
                        is_wrong = False
                        score += 3
                        global how_many_pairs
                        how_many_pairs += 1
                else:
                    first_flipped_card_index = i
                break


def wrong_pair():
    pygame.mixer.stop()
    pygame.mixer.Sound(os.path.join("sounds", "error.wav")).play()

    global first_flipped_card_index, second_flipped_card_index
    shown_board[first_flipped_card_index] = image_back
    shown_board[second_flipped_card_index] = image_back

    screen.blit(shown_board[first_flipped_card_index], cards_positions[first_flipped_card_index])

    screen.blit(shown_board[second_flipped_card_index], cards_positions[second_flipped_card_index])

    first_flipped_card_index = None
    second_flipped_card_index = None

    global is_wrong, last_wrong_time
    is_wrong = False
    last_wrong_time = 0


def check_win():
    # Victory
    if how_many_pairs == 8:
        pygame.mixer.stop()
        pygame.mixer.Sound(os.path.join("sounds", "victory.wav")).play()
        global match_is_running
        match_is_running = False
        ctypes.windll.user32.MessageBoxW(0, "Parabéns! Você venceu o " +
                                            "jogo fazendo " + str(score) +
                                            " pontos!", "Fim de Jogo!", 1)


def run():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_wrong:
                clicked_x, clicked_y = pygame.mouse.get_pos()
                click_handler(clicked_x, clicked_y)

        if is_wrong and pygame.time.get_ticks() - last_wrong_time >= 800:
            wrong_pair()

        if match_is_running:
            global match_time
            # Calculates the match duration:
            match_time = (pygame.time.get_ticks() - match_start_time) // 1000
            draw_menu()

        pygame.display.flip()

        if match_is_running:
            check_win()


start_match()
run()
