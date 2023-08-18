import socket
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Obtenha o caminho absoluto para o diretório pai
sys.path.append(parent_dir) # Adicione o diretório pai ao sys.path

from config import socket_host, socket_port


def send_receive_messages(client_socket):
    try:
        while True:
            message = input("-> ")
            client_socket.send(message.encode())
            data = client_socket.recv(1024).decode()
            print('Server:', data)
            if message.lower().strip() == 'bye':
                break
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def main():
    host = socket_host
    port = socket_port

    client_socket = socket.socket()
    client_socket.connect((host, port))

    print("Connected to server on", host, "port", port)

    try:
        send_receive_messages(client_socket)
    except KeyboardInterrupt:
        print("Closing the client.")



if __name__ == "__main__":
    main()


