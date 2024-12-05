import pygame
import sys
import random
import socket

# Configuração do servidor UDP
UDP_IP = "0.0.0.0"
UDP_PORT = 1060

# Configuração de portas dos clientes
CLIENTE1_UDP_PORT = 1061
CLIENTE2_UDP_PORT = 1062

# Criação do socket UDP para receber e enviar dados
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
vencedor = None  # Define o vencedor
mensagem_vencedor = ""  # Mensagem personalizada do vencedor

# Função para notificar o vencedor
def notify_winner(vencedor):
    if vencedor == "Jogador 1":
        sock.sendto("você venceu".encode(), ("127.0.0.1", CLIENTE1_UDP_PORT))
    elif vencedor == "Jogador 2":
        sock.sendto("você venceu".encode(), ("127.0.0.1", CLIENTE2_UDP_PORT))

def handle_udp_message():
    global player_current_house, opponent_current_house
    try:
        data, addr = sock.recvfrom(1024)  # Recebe dados via UDP
        message = data.decode().strip()
        if message == "jogador1_w":
            player_current_house = max(0, player_current_house - 3)
        elif message == "jogador1_s":
            player_current_house = min(num_houses - 1, player_current_house + 3)
        elif message == "jogador2_w":
            opponent_current_house = max(0, opponent_current_house - 3)
        elif message == "jogador2_s":
            opponent_current_house = min(num_houses - 1, opponent_current_house + 3)
    except BlockingIOError:
        pass

def update_positions():
    player.top = player_current_house * house_height
    player.top = max(0, min(player.top, screen_height - player.height))
    opponent.top = opponent_current_house * house_height
    opponent.top = max(0, min(opponent.top, screen_height - opponent.height))

def input_text():
    global mensagem_vencedor
    font = pygame.font.Font(None, 36)
    user_input = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressionar Enter para confirmar
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Apagar último caractere
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        screen.fill(pygame.Color("grey20"))
        text_surface = font.render("Digite sua mensagem:", True, light_grey)
        input_surface = font.render(user_input, True, light_grey)

        screen.blit(text_surface, (screen_width / 2 - text_surface.get_width() / 2, screen_height / 4))
        screen.blit(input_surface, (screen_width / 2 - input_surface.get_width() / 2, screen_height / 2))
        pygame.display.flip()

    mensagem_vencedor = user_input

# Função de animação da bola
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, game_active, vencedor
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        player_score += 1
        ball_start()
    if ball.right >= screen_width:
        opponent_score += 1
        ball_start()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    if player_score >= 3:
        game_active = False
        vencedor = "Jogador 1"
        notify_winner(vencedor)  # Notificar o vencedor
    elif opponent_score >= 3:
        game_active = False
        vencedor = "Jogador 2"
        notify_winner(vencedor)  # Notificar o vencedor

def ball_start():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_active:
        handle_udp_message()
        ball_animation()
        update_positions()
    else:
        if vencedor and not mensagem_vencedor:
            input_text()

        screen.fill(bg_color)
        vencedor_text = game_font.render(f"{vencedor} venceu!", True, light_grey)
        mensagem_text = game_font.render(mensagem_vencedor, True, light_grey)

        screen.blit(vencedor_text, (screen_width / 2 - vencedor_text.get_width() / 2, screen_height / 4))
        screen.blit(mensagem_text, (screen_width / 2 - mensagem_text.get_width() / 2, screen_height / 2))
        pygame.display.flip()
        continue

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    player_text = game_font.render(f"{player_score}", True, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)
    screen.blit(player_text, (screen_width / 2 + 20, 20))
    screen.blit(opponent_text, (screen_width / 2 - 40, 20))

    pygame.display.flip()
    clock.tick(60)
