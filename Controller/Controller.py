import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import socket
import threading
from collections import deque
import requests
from config import server_host, socket_host, socket_port
import json


# {client_socket: True, client_socket: True, client_socket: False}
conexoes = {}

class ResponseData:
    def __init__(self, id, response, client_socket):
        self.id = id
        self.response = response
        self.client_socket = client_socket

def aceitar_conexoes(server_socket, data_queue):
    while True:
        client_socket, client_address = server_socket.accept()
        conexoes[client_socket] = True

        print("Nova conexão:", client_address, "\n")
        # print("conexoes:", conexoes, "\n")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, data_queue))
        client_thread.start()

def handle_client(client_socket, data_queue):
    try:

        while True:  # Mantém o socket aberto para receber novos IDs continuamente
            id = client_socket.recv(1024).decode('utf-8')
            if not id:  # Se o cliente fechou a conexão
                print("Conexão fechada pelo cliente:", client_socket.getpeername())
                break  # Sair do loop
            data_queue.append((id, client_socket))
            
    except Exception as e:
        print("Erro ao lidar com o cliente:", e)
    finally:
        if client_socket in conexoes:
            del conexoes[client_socket]  # Remover a conexão do dicionário
        client_socket.close()  # Fechar o socket


def realizar_requisicoes_http(data_queue):
    while True:
        
        if data_queue:
            id, client_socket = data_queue.popleft()
            try:

                if not conexoes.get(client_socket):
                    client_socket.send("Caixa bloqueado".encode('utf-8'))
                else:
                    response = requests.get(server_host + id)

                    if (response.status_code == 204):
                        mensagem = "Produto não encontrado"
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

    data_queue = deque()

    accept_thread = threading.Thread(target=aceitar_conexoes, args=(server_socket, data_queue))
    accept_thread.start()

    http_request_thread = threading.Thread(target=realizar_requisicoes_http, args=(data_queue,))
    http_request_thread.start()

if __name__ == "__main__":
    main()