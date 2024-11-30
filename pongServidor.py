import pygame
import sys
import random
import socket

# Configuração do servidor UDP
UDP_IP = "0.0.0.0"
UDP_PORT = 1060

# Criação do socket UDP para receber dados
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)  # Não bloquear se não houver dados

# Configuração geral do Pygame
pygame.init()
clock = pygame.time.Clock()

# Janela principal
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong - Dois Jogadores")

# Cores
light_grey = (200, 200, 200)
bg_color = pygame.Color("grey12")

# Retângulos do jogo
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)  # Direita
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)  # Esquerda

# Variáveis do jogo
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
num_houses = 10
house_height = screen_height // num_houses

# Posições dos jogadores
player_current_house = num_houses // 2  # Começa no meio
opponent_current_house = num_houses // 2

# Pontuações
player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 36)

# Controle do jogo
game_active = True

# Funções do jogo
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Rebote nas bordas superior e inferior
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Pontuação
    if ball.left <= 0:
        player_score += 1
        ball_start()
    if ball.right >= screen_width:
        opponent_score += 1
        ball_start()

    # Colisão com jogadores
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def ball_start():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

def handle_udp_message():
    global player_current_house, opponent_current_house
    try:
        data, addr = sock.recvfrom(1024)  # Recebe dados via UDP
        message = data.decode().strip()
        print(f"Mensagem recebida: {message}")  # Verificar a mensagem recebida
        # Mensagens para o jogador da direita
        if message == "jogador1_w":
            player_current_house = max(0, player_current_house - 3)  # Subir 3 casas
            print(f"Nova posição do jogador: {player_current_house}")
        elif message == "jogador1_s":
            player_current_house = min(num_houses - 1, player_current_house + 3)  # Descer 3 casas
            print(f"Nova posição do jogador: {player_current_house}")
        # Mensagens para o jogador da esquerda
        elif message == "jogador2_w":
            opponent_current_house = max(0, opponent_current_house - 3)  # Subir 3 casas
            print(f"Nova posição do oponente: {opponent_current_house}")
        elif message == "jogador2_s":
            opponent_current_house = min(num_houses - 1, opponent_current_house + 3)  # Descer 3 casas
            print(f"Nova posição do oponente: {opponent_current_house}")
    except BlockingIOError:
        pass  # Sem mensagens, continuar o loop

def update_positions():
    # Atualizar posição do jogador (direita)
    player.top = player_current_house * house_height
    player.top = max(0, min(player.top, screen_height - player.height))
    # Atualizar posição do oponente (esquerda)
    opponent.top = opponent_current_house * house_height
    opponent.top = max(0, min(opponent.top, screen_height - opponent.height))

# Loop principal
while True:
    # Lidar com eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Processar mensagens UDP
    handle_udp_message()

    if game_active:
        # Atualizar lógica do jogo
        ball_animation()
        update_positions()

    # Desenhar o jogo
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Exibir pontuações
    player_text = game_font.render(f"{player_score}", True, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)
    screen.blit(player_text, (screen_width / 2 + 20, 20))
    screen.blit(opponent_text, (screen_width / 2 - 40, 20))

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)
