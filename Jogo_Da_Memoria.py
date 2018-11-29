import pygame
import os.path
import sys
import random
import ctypes

# Vetor que representa o nome de todas as cartas do baralho
NOME_IMAGENS = ["carta1", "carta2", "carta3", "carta4", "carta5", "carta6", "carta7", "carta8"]

# Constante que representa o tipo das imagens das cartas
EXTENSAO_IMAGENS = ".png"

# Dimensões da tela:
WIDTH_TELA = 900
HEIGHT_TELA = 700

# Card data
CARD_WIDTH = 105
CARD_HEIGHT = 155

MENU_WIDTH = 250
MENU_HEIGHT = HEIGHT_TELA

card_backward_image = None
board = []

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


# Sounds
score_sound = None
flip_sound = None
victory_sound = None
error_sound = None

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

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jogo da Memória")
pygame.display.set_icon(pygame.image.load(os.path.join("images", NOME_IMAGENS[0] + EXTENSAO_IMAGENS)))

screen = pygame.display.set_mode((WIDTH_TELA, HEIGHT_TELA))
screen.fill((255, 255, 255))

score_sound = pygame.mixer.Sound(os.path.join("sounds", "point.wav"))
victory_sound = pygame.mixer.Sound(os.path.join("sounds", "victory.wav"))
error_sound = pygame.mixer.Sound(os.path.join("sounds", "error.wav"))
flip_sound = pygame.mixer.Sound(os.path.join("sounds", "flip.wav"))


logo = pygame.image.load(os.path.join("images", "logo.png"))
logo = pygame.transform.scale(logo, (250, 100))

card_backward_image = pygame.image.load(os.path.join("images", "costas.png"))

for card_name in NOME_IMAGENS:
    card_image = pygame.image.load(os.path.join("images", card_name + EXTENSAO_IMAGENS))

    board.append(Card(card_name, card_image))
    board.append(Card(card_name, card_image))

screen.fill((255, 255, 255))
pygame.time.delay(100)


def draw_menu():
    # Reset:
    menu_rect = pygame.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect)

    # Logo:
    global logo
    logo = pygame.transform.scale(logo, (250, 100))
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

                pygame.mixer.stop()
                flip_sound.play()

                pygame.draw.rect(screen, (255, 255, 255), card.card_rectangle)
                c = pygame.transform.scale(card.card_image, (CARD_WIDTH, CARD_HEIGHT))
                screen.blit(c, card.card_rectangle)

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
                        score_sound.play()
                        global how_many_pairs
                        is_wrong = False
                        score += 3
                        how_many_pairs += 1
                        current_pair.clear()
                break

def wrong_pair():
    pygame.mixer.stop()
    error_sound.play()

    current_pair[0].flip_card()
    current_pair[1].flip_card()

    pygame.draw.rect(screen, (255, 255, 255), current_pair[0].card_rectangle)
    card1 = pygame.transform.scale(card_backward_image, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(card1, current_pair[0].card_rectangle)

    pygame.draw.rect(screen, (255, 255, 255), current_pair[1].card_rectangle)
    card1 = pygame.transform.scale(card_backward_image, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(card1, current_pair[1].card_rectangle)

    current_pair.clear()
    global is_wrong, last_wrong_time
    is_wrong = False
    last_wrong_time = 0


def check_win():
    if how_many_pairs == 8:
        pygame.mixer.stop()
        victory_sound.play()
        global match_is_running
        match_is_running = False
        ctypes.windll.user32.MessageBoxW(0, "Parabéns! Você venceu o jogo fazendo " + str(score) + " pontos!", "Fim de Jogo!", 1)


clock = pygame.time.Clock()
def run():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_wrong:
                clicked_x, clicked_y = pygame.mouse.get_pos()
                click_handler(clicked_x, clicked_y)
            
        time_now = pygame.time.get_ticks()
        draw_menu()

        if is_wrong and time_now - last_wrong_time >= 1000:
            wrong_pair()

        if match_is_running:
            global match_time
            match_time = (time_now - match_start_time) // 1000
            draw_menu()

        pygame.display.flip()

        if match_is_running:
            check_win()


start_match()
run()
