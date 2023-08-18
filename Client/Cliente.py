import socket
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port

def send_receive_messages(client_socket):
    try:
        while True:
            message = input("-> ")
            client_socket.send(message.encode())
            print("Enviei")
            
            # if message.lower().strip() == 'bye':
            #     print("Encerrando conexão...")
            #     break
            
            data = client_socket.recv(1024).decode() #ERRO AQUI
            print("Recebi")

            # print('----------\n', data, '\n----------')
    except socket.error as e:
        print("Erro de soquete:", e)
    except KeyboardInterrupt:
        print("Cliente interrompido pelo usuário.")
    finally:
        client_socket.close()

def main():
    host = socket_host
    port = socket_port

    client_socket = socket.socket()

    try:
        client_socket.connect((host, port))
        print("Conectado ao socket em", host, "porta", port)
        send_receive_messages(client_socket)
    except socket.error as e:
        print("Erro de conexão:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()