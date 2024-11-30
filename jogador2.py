import pygame
import socket

# Configurações do cliente UDP
UDP_IP = "127.0.0.1"  # LocalHost
UDP_PORT = 1060  # Porta UDP

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()

screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cliente UDP - Enviar w/s")

bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)
font_path = pygame.font.match_font('arial')  
font = pygame.font.Font(font_path, 36)

def envia_mensagem_udp(message):
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    print(f"Enviado: {message}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Seta para cima
                envia_mensagem_udp("jogador2_w")
            elif event.key == pygame.K_DOWN:  # Seta para baixo
                envia_mensagem_udp("jogador2_s")

    screen.fill(bg_color)
    text = font.render("Para cima (↑) | Para baixo (↓)", True, light_grey)
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2))
    pygame.display.flip()

pygame.quit()
