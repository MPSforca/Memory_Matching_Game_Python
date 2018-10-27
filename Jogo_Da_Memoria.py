import pygame
import os.path
import sys
import random

# Element at 0: Card back
images_name = ["costas.jpg", "carta1.jpg", "carta2.jpg", "carta3.jpg",
               "carta4.jpg", "carta5.jpg", "carta6.jpg", "carta7.jpg",
               "carta8.jpg"]
# List with every image loaded from the images_name
images = []
# Position of every card
cards_positions = []
# Board that the player is seeing
shown_board = []
# Board that represents every card flipped
actual_board = []
# Card data:
card_width = 170
card_height = 150
# Current pair data:
current_flipped_card_index = None

pygame.init()
pygame.display.set_caption("Jogo da Memória")

# Screen size and color
screen = pygame.display.set_mode((900, 700))
screen.fill((255, 255, 255))


def start():
    # Load and create images from path
    for image in images_name:
        card = pygame.image.load(os.path.join("imagens", image))
        # Set image size:
        card = pygame.transform.scale(card, (card_width, card_height))

        # It's not the first image (Card's back)
        if len(images) > 0:
            # Adds twice => Two cards of each on board
            actual_board.append(card)
            actual_board.append(card)

        images.append(card)

    # Shuffle the board
    random.shuffle(actual_board)

    global shown_board
    shown_board = [images[0]] * 16

    # Updates the board that is being shown for the player
    create_board()


def create_board():
    cards_back = images[0]

    # Fill the board with images
    for i in range(0, 16):

        # Card position:
        x = 50 + card_width * (i % 4) + 40 * (i % 4)
        y = 20 + card_height * (i // 4) + 20 * (i // 4)

        rect = pygame.Rect(x, y, card_width, card_height)

        global cards_positions
        cards_positions.append(rect)

        screen.blit(cards_back, rect)


def click_handler(mouse_x, mouse_y):
    for i in range(0, 16):
        if cards_positions[i].collidepoint(mouse_x, mouse_y):
            if shown_board[i] == images[0]:  # The card is backwards:
                shown_board[i] = actual_board[i]
                # Draws the card:
                screen.blit(shown_board[i], cards_positions[i])
                pygame.display.flip()
                global current_flipped_card_index
                # There's already a card facing front:
                if current_flipped_card_index is not None:
                    # Wrong pair:
                    if (actual_board[current_flipped_card_index] !=
                            actual_board[i]):
                        # Time for the player to see the card
                        pygame.time.delay(1000)
                        shown_board[current_flipped_card_index] = images[0]
                        shown_board[i] = images[0]

                        screen.blit(
                            shown_board[current_flipped_card_index],
                            cards_positions[current_flipped_card_index])

                        screen.blit(shown_board[i], cards_positions[i])

                    current_flipped_card_index = None
                else:
                    current_flipped_card_index = i
            break


def run():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_x, clicked_y = pygame.mouse.get_pos()
                click_handler(clicked_x, clicked_y)

        pygame.display.flip()


start()
run()
