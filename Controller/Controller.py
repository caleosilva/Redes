import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import socket
import threading
import requests
from config import server_host, socket_host, socket_port
import json


# {client_socket: True, client_socket: True, client_socket: False}
conexoes = {}

def aceitar_conexoes(server_socket, ):
    while True:
        client_socket, client_address = server_socket.accept()
        conexoes[client_socket] = True

        print("Nova conexão:", client_address, "\n")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, ))
        client_thread.start()

def handle_client(client_socket):
    try:
        while True:  # Mantém o socket aberto para receber novos IDs continuamente
            id = client_socket.recv(1024).decode('utf-8')
            if id:  # Se o cliente fechou a conexão
                realizar_requisicoes_http(id, client_socket)
    except Exception as e:
        print("Erro ao lidar com o cliente:", e)
    finally:
        if client_socket in conexoes:
            del conexoes[client_socket]  # Remover a conexão do dicionário
        client_socket.close()  # Fechar o socket


def realizar_requisicoes_http(id, client_socket):
    try:
        if not conexoes.get(client_socket):
            client_socket.send("Caixa bloqueado".encode('utf-8'))
        else:
            response = requests.get(server_host + id)

            if (response.status_code == 204):
                mensagem = "204"
                client_socket.send(mensagem.encode('utf-8'))

            elif (response.status_code == 200):                
                data_dict = response.json()
                data = json.dumps(data_dict)
                client_socket.send(data.encode('utf-8'))

            else:
                client_socket.send("Erro".encode('utf-8'))
    except Exception as e:
        print("Erro ao fazer a solicitação HTTP:", e)

def main():
    host = socket_host
    port = socket_port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Já estou ouvindo o socket em", host, "na", port)

    accept_thread = threading.Thread(target=aceitar_conexoes, args=(server_socket, ))
    accept_thread.start()


if __name__ == "__main__":
    main()