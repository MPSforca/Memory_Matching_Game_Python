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

# Dimensões das cartas em pixels:
WIDTH_CARTA = 105
HEIGHT_CARTA = 155

# Dimensões do menu lateral
WIDTH_MENU = 250
HEIGHT_MENU = HEIGHT_TELA

imagem_costas_carta = None  # Variável que representará a imagem das costas das cartas
tabuleiro = []              # Vetor que representa o tabuleiro atual

# Variáveis para tratar do par atual:
par_atual = []
esta_errado = False
tempo_ultimo_erro = 0

# Variáveis que representam dados sobre a partida
qtos_pares = 0              # Quantos pares o jogador já encontrou
pontuacao = 0               # Pontuacao do usuário
tempo_partida = 0           # Tempo desde o início da partida
tempo_inicio_partida = None # Tempo que representa quando iniciou a partida
partida_acontecendo = True  # Booleana que indica se a partida está acontecendo

# Variáveis que serão utilizadas durante o menu
botao_sair = None
botao_reiniciar = None
logo = None


# Sons
som_pontuacao = None
som_virada = None
som_vitoria = None
som_erro = None

# Classe Carta que representará cada carta do jogo
class Carta:
    nome_carta = ""         # Representa o nome da carta
    imagem_carta = ""       # Representa a imagem da carta
    retangulo_carta = None  # Representa o retangulo no qual a carta está posicionada
    de_costas = True        # Indica se a carta está virada de costas

    def __init__(self, nome_carta, imagem_carta, de_costas = True):
        self.nome_carta = nome_carta
        self.imagem_carta = imagem_carta
        self.de_costas = de_costas

    # Método para mudar a localização da imagem
    def set_retangulo(self, rect):
        self.retangulo_carta = rect

    # Método para virar a carta
    def virar_carta(self):
        self.de_costas = not self.de_costas

# Inicia o jogo
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jogo da Memória")       # Para mudar o título do programa
pygame.display.set_icon(pygame.image.load(os.path.join("images", NOME_IMAGENS[0] + EXTENSAO_IMAGENS)))

# Preenche a tela de branco (para iniciá-la) 
screen = pygame.display.set_mode((WIDTH_TELA, HEIGHT_TELA))
screen.fill((255, 255, 255))

# Carrega os sons do jogo
som_pontuacao = pygame.mixer.Sound(os.path.join("sounds", "point.wav"))
som_vitoria = pygame.mixer.Sound(os.path.join("sounds", "victory.wav"))
som_erro = pygame.mixer.Sound(os.path.join("sounds", "error.wav"))
som_virada = pygame.mixer.Sound(os.path.join("sounds", "flip.wav"))

# Carrega o logo do jogo e ajusta a sua escala
logo = pygame.image.load(os.path.join("images", "logo.png"))
logo = pygame.transform.scale(logo, (250, 100))

# Carrega a imagem da parte de trás das cartas
imagem_costas_carta = pygame.image.load(os.path.join("images", "costas.png"))

# Para cada carta informada no vetor de cartas...
for nome_carta in NOME_IMAGENS:
    imagem_carta = pygame.image.load(os.path.join("images", nome_carta + EXTENSAO_IMAGENS)) # Adiciona sua imagem no vetor

    # Adiciona duas vezes a mesma carta no tabuleiro porque o jogo é composto de pares
    tabuleiro.append(Carta(nome_carta, imagem_carta))
    tabuleiro.append(Carta(nome_carta, imagem_carta))

# Reseta a tela
screen.fill((255, 255, 255))
pygame.time.delay(100)


# Método para desenhar o menu
def desenhar_menu():
    # Resetar o menu (Pinta-o inteiro de branco):
    ret_menu = pygame.Rect(0, 0, WIDTH_MENU, HEIGHT_MENU)
    pygame.draw.rect(screen, (255, 255, 255), ret_menu)

    # Carregar a Logo e exibí-la no menu:
    global logo
    logo = pygame.transform.scale(logo, (250, 100))
    rect = pygame.Rect(0, 0, WIDTH_MENU, 100)
    screen.blit(logo, rect)
    escrever_informacoes_jogo()

    # Linha lateral do menu:
    pygame.draw.line(screen, (0, 0, 0), (WIDTH_MENU + 10, 0), (WIDTH_MENU + 10, HEIGHT_MENU))

    # Botões para reiniciar a partida e sair do jogo:
    f = pygame.font.Font(os.path.join("fonts", "Montserrat-Regular.ttf"), 20)
    texto_botao = f.render("Reiniciar", 1, (0, 0, 0))
    global botao_reiniciar
    botao_reiniciar = screen.blit(texto_botao, (20, 600))

    texto_botao = f.render("Sair", 1, (0, 0, 0))
    global botao_sair
    botao_sair = screen.blit(texto_botao, (20, 630))

# Método que resetará as principais variáveis de uma partida
def iniciar_partida():
    random.shuffle(tabuleiro)       # Embaralha o tabuleiro

    # Vira todas as cartas de costas:
    for carta in tabuleiro:
        carta.de_costas = True

    # Desenha o menu e chama o método para criar o tabuleiro
    desenhar_menu()
    criar_tabuleiro()

    # Reseta a pontuação da partida e ajusta o tempo de início da mesma
    global pontuacao, tempo_inicio_partida
    pontuacao = 0
    tempo_inicio_partida = pygame.time.get_ticks()

    # Reseta a quantidade de pares encontrados pelo usuário e dados sobre o tempo da partida
    global qtos_pares, tempo_partida, partida_acontecendo
    qtos_pares = 0
    tempo_partida = 0
    partida_acontecendo = True


# Método para escrever as informações da partida no menu
def escrever_informacoes_jogo():
    # Escreve a pontuação atual do jogador:
    f = pygame.font.Font(os.path.join("fonts", "Montserrat-Regular.ttf"), 20)
    text = f.render("Pontuação: " + str(pontuacao), 1, (0, 0, 0))
    screen.blit(text, (20, 150, 30, 210))

    # Escreve o tempo de partida:
    text = f.render("Tempo: " + str(tempo_partida) + "s", 1, (0, 0, 0))
    screen.blit(text, (20, 180, 30, 210))


# Método para criar o tabuleiro:
def criar_tabuleiro():
    indice_atual = 0
    for carta in tabuleiro:
        # Pega a posição X e Y da carta de acordo com a sua posição no tabuleiro (4 cartas por linha e coluna)
        x = 300 + WIDTH_CARTA * (indice_atual % 4) + 40 * (indice_atual % 4)
        y = 20 + HEIGHT_CARTA * (indice_atual // 4) + 20 * (indice_atual // 4)
        rect = pygame.Rect(x, y, WIDTH_CARTA, HEIGHT_CARTA)

        # Salva a posição da carta
        carta.set_retangulo(rect)

        # Desenha uma carta virada de costas da posição da carta
        cards_back = pygame.transform.scale(imagem_costas_carta, (WIDTH_CARTA, HEIGHT_CARTA))
        screen.blit(cards_back, carta.retangulo_carta)
        indice_atual += 1


# Método para tratar os cliques do usuário
def click_handler(mouse_x, mouse_y):
    if botao_sair.collidepoint(mouse_x, mouse_y):           # Caso o usuário tenha clicado no botão de sair da partida...
        sys.exit()                                          # Fecha o jogo
    elif botao_reiniciar.collidepoint(mouse_x, mouse_y):    # Caso o usuário tenha clicado no botão de reiniciar...
        iniciar_partida()                                   # Chama o método para iniciar uma nova partida
    else:  # O usuário clicou sobre uma carta:
        for carta in tabuleiro:                             # Verifica sobre qual carta o usuário clicou             
            if carta.retangulo_carta.collidepoint(mouse_x, mouse_y) and carta.de_costas: # Encontrou a carta, e ela está de costas
                # Vira a carta
                carta.virar_carta()

                # Para qualquer som que esteja ocorrendo e toca o som de virada de carta
                pygame.mixer.stop()
                som_virada.play()

                # Desenha na tela a carta de frente, em sua posição
                pygame.draw.rect(screen, (255, 255, 255), carta.retangulo_carta)
                c = pygame.transform.scale(carta.imagem_carta, (WIDTH_CARTA, HEIGHT_CARTA))
                screen.blit(c, carta.retangulo_carta)

                # Verifica se é a primeira ou a segunda carta do par atual: 
                par_atual.append(carta)
                global esta_errado, pontuacao
                if len(par_atual) == 2: # Indica que é a segunda carta do par, e assim o par já está formado
                    if par_atual[0].nome_carta != par_atual[1].nome_carta:    # O par está errado:
                        global tempo_ultimo_erro
                        # Avisa ao programa que, durante o loop, deverá tratar o viramento das cartas
                        tempo_ultimo_erro = pygame.time.get_ticks()
                        esta_errado = True
                        # Diminui a posição do usuário por errar
                        pontuacao -= 1  
                    else:   # O usuário acertou o par:
                        # Toca som de acerto
                        pygame.mixer.stop()
                        som_pontuacao.play()
                        global qtos_pares
                        esta_errado = False
                        # Adiciona a pontuação ao usuário
                        pontuacao += 3
                        # Adiciona mais um par ao usuário
                        qtos_pares += 1
                        par_atual.clear()
                break

# Método que será chamado quando o usuário errar um par:
def par_errado():
    # Toca o som de erro:
    pygame.mixer.stop()
    som_erro.play()

    # Pega as duas cartas do par atual e as vira de costas novamente
    par_atual[0].virar_carta()
    par_atual[1].virar_carta()

    # Desenha na tela as cartas viradas de costas
    # CARTA 1:
    pygame.draw.rect(screen, (255, 255, 255), par_atual[0].retangulo_carta)
    card1 = pygame.transform.scale(imagem_costas_carta, (WIDTH_CARTA, HEIGHT_CARTA))
    screen.blit(card1, par_atual[0].retangulo_carta)

    # CARTA 2:
    pygame.draw.rect(screen, (255, 255, 255), par_atual[1].retangulo_carta)
    card1 = pygame.transform.scale(imagem_costas_carta, (WIDTH_CARTA, HEIGHT_CARTA))
    screen.blit(card1, par_atual[1].retangulo_carta)

    # Limpa a lista que contém as cartas do par atual
    par_atual.clear()
    global esta_errado, tempo_ultimo_erro
    # Prepara o programa para um eventual futuro erro do usuário
    esta_errado = False
    tempo_ultimo_erro = 0

# Método para verificar caso o jogador já acertou todas as cartas
def verifica_vitoria():
    # Verifica se a quantidade de pares acertados pelo usuário é igual à quantidade máxima de pares
    if qtos_pares == 8:
        # Toca som de vitória
        pygame.mixer.stop()
        som_vitoria.play()
        global partida_acontecendo
        partida_acontecendo = False
        # Exibe a mensagem de erro
        ctypes.windll.user32.MessageBoxW(0, "Parabéns! Você venceu o jogo fazendo " + str(pontuacao) + " pontos!", "Fim de Jogo!", 1)


relogio = pygame.time.Clock() # Inicia o relógio
def run():
    while 1:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and not esta_errado:     # O usuário clicou em alguma posição
                x_clicado, y_clicado = pygame.mouse.get_pos()               
                click_handler(x_clicado, y_clicado)                             # Chama o método para tratar o clique
            
        # Pega o tempo atual do programa
        tempo_atual = pygame.time.get_ticks()
        # Redesenha o menu a cada frame
        desenhar_menu()

        # O usuário errou um par e já foi dado um segundo para que ele visualizasse as cartas:
        if esta_errado and tempo_atual - tempo_ultimo_erro >= 1000:
            par_errado()

        # Caso a partida esteja em andamento, atualiza informações do menu
        if partida_acontecendo:
            global tempo_partida
            tempo_partida = (tempo_atual - tempo_inicio_partida) // 1000    # Atualiza o tempo do andamento da partida
            desenhar_menu()

        # Atualiza a tela
        pygame.display.flip()

        # Verifica se o usuário acertou todos os pares
        if partida_acontecendo:
            verifica_vitoria()


iniciar_partida()
run()
