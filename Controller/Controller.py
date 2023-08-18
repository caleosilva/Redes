import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import socket
import threading
from collections import deque
import requests
from config import server_host, socket_host, socket_port


class ResponseData:
    def __init__(self, id, response, client_socket):
        self.id = id
        self.response = response
        self.client_socket = client_socket

def accept_connections(server_socket, data_queue):
    while True:
        client_socket, client_address = server_socket.accept()
        print("Nova conexão:", client_address, "\n")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, data_queue))
        client_thread.start()

def handle_client(client_socket, data_queue):
    while True:  # Mantém o socket aberto para receber novos IDs continuamente
        try:
            id = client_socket.recv(1024).decode('utf-8')
            if id:
                # print("ID recebido:", id)
                data_queue.append((id, client_socket))
        except Exception as e:
            print("Erro ao lidar com o cliente:", e)
            break  # Encerra o loop se ocorrer um erroI


def make_http_requests(data_queue, response_queue):
    while True:
        
        if data_queue:
            id, client_socket = data_queue.popleft()
            try:
                # print("make_http_requests: ", client_socket, "\n")
                response = requests.get(server_host + id)
                response_queue.append(ResponseData(id, response.text, client_socket))
            except Exception as e:
                print("Erro ao fazer a solicitação HTTP:", e)

def process_http_responses(response_queue):
    while True:
        if response_queue:
            response_data = response_queue.popleft()
            try:
                # print("process_http_responses: ", response_data.client_socket)
                response_data.client_socket.send(response_data.response.encode('utf-8'))
            except Exception as e:
                print("Erro ao enviar resposta para o cliente:", e)
def main():
    host = socket_host
    port = socket_port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Já estou ouvindo o socket em", host, "na", port)

    data_queue = deque()
    response_queue = deque()

    accept_thread = threading.Thread(target=accept_connections, args=(server_socket, data_queue))
    accept_thread.start()

    http_request_thread = threading.Thread(target=make_http_requests, args=(data_queue, response_queue))
    http_request_thread.start()

    response_process_thread = threading.Thread(target=process_http_responses, args=(response_queue,))
    response_process_thread.start()

if __name__ == "__main__":
    main()