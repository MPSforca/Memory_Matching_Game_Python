import pygame
import os.path
import sys
import random

# Element at 0: Card back
images_name = ["costas.jpg", "carta1.jpg", "carta2.jpg", "carta3.jpg",
               "carta4.jpg", "carta5.jpg", "carta6.jpg", "carta7.jpg",
               "carta8.jpg"]
images = []
shown_board = []
actual_board = []
card_width = 170
card_height = 150

pygame.init()
pygame.display.set_caption("Jogo da Memória")

# Screen size and color
screen = pygame.display.set_mode((900, 700))
screen.fill((255, 255, 255))


def start():
    # Load and create images from path
    for image in images_name:
        card = pygame.image.load(os.path.join("imagens", image))

        # It's not the first image (Card's back)
        if len(images) > 0:
            # Adds twice => Two cards of each on board
            actual_board.append(card)
            actual_board.append(card)

        images.append(card)

    # Shuffle the board
    random.shuffle(actual_board)

    # The board that is being shown for the user (images[0] = card's back img)
    global shown_board
    shown_board = [images[0]] * 16

    # Updates the board that is being shown for the player
    _update_shown_board()


def _update_shown_board():
    # Fill the board with images
    for i in range(0, 16):
        # Get the image that represents card's back:
        current_card = shown_board[i]

        # Set image size:
        current_card = pygame.transform.scale(current_card, 
                                              (card_width, card_height))

        rect = current_card.get_rect()

        # Card position:
        x = 50 + card_width * (i % 4) + 40 * (i % 4)
        y = 20 + card_height * (i // 4) + 20 * (i // 4)
        rect = rect.move(x, y)

        # Print image on screen:
        screen.blit(current_card, rect)


def run():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()


start()
run()
