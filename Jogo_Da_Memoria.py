import pygame
import os.path
import sys


images = ["costas.jpg"]
board = []

pygame.init()

# Screen size and color
screen = pygame.display.set_mode((900, 700))
screen.fill((255, 255, 255))


def start():
    for image in images:
        card = pygame.image.load(os.path.join("imagens", image))
        card = pygame.transform.scale(card, (170, 160))
    
    for i in range(0, 16):
        rect = card.get_rect()
        x = 50 + 170 * (i % 4) + 40 * (i % 4)
        y = 20 + 160 * (i // 4) + 20 * (i // 4)
        rect = rect.move(x, y)
        screen.blit(card, rect)


start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
    pygame.display.flip()