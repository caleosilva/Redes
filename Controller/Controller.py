import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import socket
import threading
import requests
from config import server_host, socket_host, socket_port
import json

conexoes = {}

def aceitar_conexoes(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        conexoes[client_socket] = True

        print("Nova conexão:", client_address, "\n")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, ))
        client_thread.start()

def receive_large_data(sock):
    data_size = int(sock.recv(1024).decode())  # Recebe o tamanho dos dados
    sock.send('OK'.encode())  # Envia um ack para o cliente
    
    received_data = ''
    while len(received_data) < data_size:
        remaining_bytes = data_size - len(received_data)
        received_data_chunk = sock.recv(min(1024, remaining_bytes)).decode()
        received_data += received_data_chunk
    
    return json.loads(received_data)

def handle_client(client_socket):
    try:
        idCaixa = ''
        while True:
            dataJson = receive_large_data(client_socket)
            print("DataJSon:", dataJson)

            if (dataJson['header'] == 'id'):
                bloqueado = verificarBloqueioCaixa(dataJson)
                if(bloqueado):
                    client_socket.send('False'.encode())
                else:
                    url = server_host + dataJson['header'] + '/' + dataJson['body']
                    realizar_requisicao_GET(url, client_socket)
            elif (dataJson['header'] == 'comprar'):
                realizar_requisicao_POST(dataJson, client_socket, idCaixa)
            elif (dataJson['header'] == 'caixas'):
                if (dataJson['body'] == ''):
                    url = server_host + dataJson['header']
                    realizar_requisicao_GET(url, client_socket)
                else:
                    idCaixa = dataJson['body']
                    url = server_host + dataJson['header'] + '/' + dataJson['body']
                    resultado = realizar_requisicao_GET(url, client_socket)
                    if (resultado and resultado[dataJson['body']]['ativo'] == False):
                        body = {'ativo': True}
                        urlManipulacao = server_host + "gerenciarCaixa" + '/' + dataJson['body']
                        alterarOcupacaoCaixa(urlManipulacao, body)
    except Exception as e:
        print("Erro ao lidar com o cliente:", e)

        if (dataJson):
            body = {'ativo': False}
            urlManipulacao = server_host + "gerenciarCaixa" + '/' + idCaixa
            alterarOcupacaoCaixa(urlManipulacao, body)
            client_socket.close()
    finally:
        body = {'ativo': False}
        urlManipulacao = server_host + "gerenciarCaixa" + '/' + idCaixa
        alterarOcupacaoCaixa(urlManipulacao, body)
        client_socket.close()

def verificarBloqueioCaixa(dataJson):
    codigoDoCaixa = dataJson['codigoDoCaixa']
    urlCaixa = server_host + 'caixas/' + codigoDoCaixa

    try:
        response = requests.get(urlCaixa)
        dadosResponse = response.json()

        if (dadosResponse[codigoDoCaixa]['bloqueado']):
            return True
        else:
            return False
    except Exception as e:
        print("Erro ao fazer a solicitação HTTP-GET-CAIXA:", e)


def realizar_requisicao_GET(url, client_socket):
    try:
        response = requests.get(url)

        if (response.status_code == 204):
            mensagem = "204"
            client_socket.send(mensagem.encode('utf-8'))
            return False

        elif (response.status_code == 200):                
            data_dict = response.json()
            data = json.dumps(data_dict)
            client_socket.send(data.encode())
            return response.json()

        else:
            client_socket.send("Erro".encode('utf-8'))
            return False
    except Exception as e:
        print("Erro ao fazer a solicitação HTTP-GET:", e)

def solicitarCaixas(dataJson, client_socket):
    try:
        if not conexoes.get(client_socket):
            client_socket.send("Caixa bloqueado".encode('utf-8'))
        else:
            response = requests.post(server_host + dataJson['header'], json=dataJson['body'])

            if (response.status_code == 400):
                mensagem = "400"
                client_socket.send("400".encode('utf-8'))

            elif (response.status_code == 201):
                client_socket.send("201".encode())

            elif (response.status_code == 404):
                client_socket.send(("404".status_code).encode())

            else:
                print(response)
                client_socket.send("Erro".encode('utf-8'))
    except Exception as e:
        print("Erro ao fazer a solicitação HTTP-POST:", e)

def alterarOcupacaoCaixa(url, operacao):
    try:
        response = requests.post(url, json=operacao)
    except Exception as e:
        print("Erro ao alterar a ocupação do caixa:", e)

def realizar_requisicao_POST(dataJson, client_socket, idCaixa):
    try:
        if not conexoes.get(client_socket):
            client_socket.send("Caixa bloqueado".encode('utf-8'))
        else:
            response = requests.post(server_host + dataJson['header'] + '/' + idCaixa, json=dataJson['body'])

            if (response.status_code == 400):
                mensagem = "400"
                client_socket.send("400".encode('utf-8'))

            elif (response.status_code == 201):
                client_socket.send("201".encode())

            elif (response.status_code == 404):
                client_socket.send(("404".status_code).encode())

            else:
                print(response)
                client_socket.send("Erro".encode('utf-8'))
    except Exception as e:
        print("Erro ao fazer a solicitação HTTP-POST:", e)

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