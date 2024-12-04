import pygame
import socket
import sys

# Configurações do cliente UDP
UDP_IP = "127.0.0.1"  # LocalHost
UDP_PORT = 1060  # Porta UDP
CLIENTE2_UDP_PORT = 1062

# Criação do socket UDP para envio e recebimento de mensagens
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)  # Não bloquear se não houver dados

pygame.init()

# Configuração da janela do Pygame
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cliente UDP - Enviar w/s")

bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)
font_path = pygame.font.match_font('arial')  
font = pygame.font.Font(font_path, 36)

# Variáveis para controlar o jogo
game_over = False
winner_message = ""

def envia_mensagem_udp(message):
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {message}")

# Função para receber mensagens do servidor
def recebe_mensagem_udp():
    global game_over, winner_message
    try:
        # Tenta receber dados do socket sem bloquear
        data, addr = sock.recvfrom(1024)  # Recebe dados via UDP
        message = data.decode().strip()
        print(f"Recebido: {message}")

        if message == "você venceu":
            game_over = True
            winner_message = "Você venceu!"
        elif message == "você perdeu":
            game_over = True
            winner_message = "Você perdeu!"
    except BlockingIOError:
        # Ignora o erro se não houver dados no socket
        pass

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Seta para cima
                envia_mensagem_udp("jogador1_w")
            elif event.key == pygame.K_DOWN:  # Seta para baixo
                envia_mensagem_udp("jogador1_s")

    # Verifica se há uma mensagem de vitória
    recebe_mensagem_udp()

    screen.fill(bg_color)

    if game_over:
        # Se o jogo acabou, exibe a mensagem de vitória ou derrota
        winner_text = font.render(winner_message, True, light_grey)
        screen.blit(winner_text, (screen_width / 2 - winner_text.get_width() / 2, screen_height / 2))
    else:
        # Caso contrário, exibe as instruções normais do jogo
        text = font.render("Para cima (↑) | Para baixo (↓)", True, light_grey)
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
