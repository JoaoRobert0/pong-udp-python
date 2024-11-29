import socket

# Configurações do servidor
server_ip = "127.0.0.1"  # Endereço IP do servidor
server_port = 1060       # Porta do servidor

# Criando o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        # Mensagem a ser enviada
        message = input("Digite uma tecla: ")

        # Enviando a mensagem ao servidor
        client_socket.sendto(message.encode(), (server_ip, server_port))
        print(f"Mensagem enviada para {server_ip}:{server_port}")

    except Exception as e:
        print(f"Erro: {e}")

