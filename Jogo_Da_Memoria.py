import pygame
import os.path
import sys
import random
import ctypes

IMAGES_NAME = ["carta1", "carta2", "carta3", "carta4", "carta5", "carta6", "carta7", "carta8"]

IMAGES_EXTENSION = ".png"

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

# Card data
CARD_WIDTH = 105
CARD_HEIGHT = 155

MENU_WIDTH = 250
MENU_HEIGHT = WINDOW_HEIGHT

frames = []

card_backward_image = None
board = []

animations = []
current_pair = []
is_wrong = False
last_wrong_time = 0
how_many_pairs = 0

score = 0
match_time = 0
match_start_time = None
match_is_running = True
leave_button = None
restart_button = None
logo = None

class Card:
    card_name = ""
    card_image = ""
    card_rectangle = None
    is_backward = True

    def __init__(self, card_name, card_image, is_backward = True):
        self.card_name = card_name
        self.card_image = card_image
        self.is_backward = is_backward

    def set_rectangle(self, rect):
        self.card_rectangle = rect

    def flip_card(self):
        self.is_backward = not self.is_backward


class Animation:
    images = []
    frame_interval = 0
    current_index = 0
    last_time_called = 0
    rect = None

    def __init__(self, images, rect, frame_interval = 10):
        self.images = images
        self.frame_interval = frame_interval
        self.current_index = 0
        self.rect = rect

    def update(self, current_time):
        if current_time - self.last_time_called >= self.frame_interval and not self.finished():
            frame = self.images[self.current_index]
            self.last_time_called = current_time
            self.current_index += 1
            return frame
        else:
            return None
    
    def finished(self):
        return len(self.images) - 1 == self.current_index


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jogo da Memória")
pygame.display.set_icon(pygame.image.load(os.path.join("images", IMAGES_NAME[0] + IMAGES_EXTENSION)))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen.fill((255, 255, 255))

logo = pygame.image.load(os.path.join("images", "logo.png"))
logo = pygame.transform.scale(logo, (250, 100))

card_backward_image = pygame.image.load(os.path.join("images", "costas.png"))

for card_name in IMAGES_NAME:
    card_image = pygame.image.load(os.path.join("images", card_name + IMAGES_EXTENSION))

    board.append(Card(card_name, card_image))
    board.append(Card(card_name, card_image))

    current_frames = []
    for i in range(1, 61):
        frame_name = str(i).zfill(4) + IMAGES_EXTENSION
        current_frames.append(pygame.image.load(os.path.join("animations", os.path.join(card_name, frame_name))))

    frames.append(current_frames)



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
    random.shuffle(board)

    for card in board:
        card.is_backward = True

    draw_menu()
    create_board()

    global score, match_start_time
    score = 0
    match_start_time = pygame.time.get_ticks()

    global how_many_pairs, match_time, match_is_running
    how_many_pairs = 0
    match_time = 0
    match_is_running = True


def write_game_data():
    f = pygame.font.Font(os.path.join("fonts", "Montserrat-Regular.ttf"), 20)
    text = f.render("Pontuação: " + str(score), 1, (0, 0, 0))
    screen.blit(text, (20, 150, 30, 210))

    text = f.render("Tempo: " + str(match_time) + "s", 1, (0, 0, 0))
    screen.blit(text, (20, 180, 30, 210))


def create_board():
    current_index = 0
    for card in board:
        x = 300 + CARD_WIDTH * (current_index % 4) + 40 * (current_index % 4)
        y = 20 + CARD_HEIGHT * (current_index // 4) + 20 * (current_index // 4)
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        card.set_rectangle(rect)
        cards_back = pygame.transform.scale(card_backward_image, (CARD_WIDTH, CARD_HEIGHT))
        screen.blit(cards_back, card.card_rectangle)
        current_index += 1


def click_handler(mouse_x, mouse_y):
    if leave_button.collidepoint(mouse_x, mouse_y):
        sys.exit()
    elif restart_button.collidepoint(mouse_x, mouse_y):
        start_match()
    else:
        for card in board:
            if card.card_rectangle.collidepoint(mouse_x, mouse_y) and card.is_backward:
                card.flip_card()

                animations.append(Animation(get_frames(card.card_name), card.card_rectangle))

                pygame.mixer.stop()
                pygame.mixer.Sound(os.path.join("sounds", "flip.wav")).play()

                current_pair.append(card)
                global is_wrong, score
                if len(current_pair) == 2:
                    if current_pair[0].card_name != current_pair[1].card_name:
                        global last_wrong_time
                        last_wrong_time = pygame.time.get_ticks()
                        is_wrong = True
                        score -= 1  
                    else: 
                        pygame.mixer.stop()
                        pygame.mixer.Sound(os.path.join("sounds", "point.wav")).play()
                        global how_many_pairs
                        is_wrong = False
                        score += 3
                        how_many_pairs += 1
                        current_pair.clear()
                        
                break

def get_frames(card_name):
    for i in range(0, len(IMAGES_NAME)):
        if card_name == IMAGES_NAME[i]:
            return frames[i]
    return None


def wrong_pair():
    pygame.mixer.stop()
    pygame.mixer.Sound(os.path.join("sounds", "error.wav")).play()

    card1 = current_pair[0]
    card2 = current_pair[1]

    cards_back = pygame.transform.scale(card_backward_image, (CARD_WIDTH, CARD_HEIGHT))

    screen.blit(cards_back, card1.card_rectangle)
    screen.blit(cards_back, card2.card_rectangle)

    current_pair[0].flip_card()
    current_pair[1].flip_card()

    animations.append(Animation(list(reversed(get_frames(card1.card_name))), card1.card_rectangle))
    animations.append(Animation(list(reversed(get_frames(card2.card_name))), card2.card_rectangle))

    current_pair.clear()
    global is_wrong, last_wrong_time
    is_wrong = False
    last_wrong_time = 0


def check_win():
    if how_many_pairs == 8:
        pygame.mixer.stop()
        pygame.mixer.Sound(os.path.join("sounds", "victory.wav")).play()
        global match_is_running
        match_is_running = False
        ctypes.windll.user32.MessageBoxW(0, "Parabéns! Você venceu o jogo fazendo " + str(score) + " pontos!", "Fim de Jogo!", 1)


def run():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_wrong and len(animations) < 2:
                clicked_x, clicked_y = pygame.mouse.get_pos()
                click_handler(clicked_x, clicked_y)

        if is_wrong and pygame.time.get_ticks() - last_wrong_time >= 800:
            wrong_pair()

        if match_is_running:
            global match_time
            match_time = (pygame.time.get_ticks() - match_start_time) // 1000
            draw_menu()
        
        for anim in animations:
            new_frame = anim.update(pygame.time.get_ticks())
            if new_frame is not None:
                pygame.draw.rect(screen, (255, 255, 255), anim.rect)
                new_frame = pygame.transform.scale(new_frame, (CARD_WIDTH, CARD_HEIGHT))
                screen.blit(new_frame, anim.rect)

            if anim.finished():
                animations.remove(anim)

        pygame.display.flip()

        if match_is_running:
            check_win()


start_match()
run()
