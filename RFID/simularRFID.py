import socket
import sys
import json
from datetime import datetime
# import mercury
import time


def aceitar_conexoes(rfid_client_socket):
    while True:
        rfid_socket, rfid_address = rfid_client_socket.accept()
        comunicacao_socket(rfid_socket)

def comunicacao_socket(rfid_client_socket):
    try:
        ultimo_tempo_leitura = {}
        while True:
            enviarId(rfid_client_socket, ultimo_tempo_leitura)
    except socket.error as e:
        print("Erro de soquete:", e)
    except KeyboardInterrupt:
        print("RFID interrompido pelo usuário.")
    finally:
        print("Comunicação fechada")
        rfid_client_socket.close()

def enviarId(rfid_client_socket, ultimo_tempo_leitura):

    inputData = input('-> ')

    if (inputData == ''):
        pass
    elif (inputData == 'comprar'):
        dados_serializados = json.dumps({'header':'comprar', 'body': False})

        rfid_client_socket.send(dados_serializados.encode('utf-8'))
        confirmacao = rfid_client_socket.recv(1024).decode('utf-8')
        print(confirmacao)
    else:
        dados_serializados = json.dumps({'header':'id', 'body': inputData})
        tempo_atual = time.time()


        if ((inputData not in ultimo_tempo_leitura) or (tempo_atual - ultimo_tempo_leitura[inputData]) > 0.1):
            ultimo_tempo_leitura[inputData] = tempo_atual

            rfid_client_socket.send(dados_serializados.encode('utf-8'))
            confirmacao = rfid_client_socket.recv(1024).decode('utf-8')
            print(confirmacao)


    


def main():
    # socket_rfid_client_host = '172.16.103.0'
    socket_rfid_client_host = '127.0.0.1'
    socket_rfid_client_port = 1235

    try:
        rfid_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rfid_client_socket.bind((socket_rfid_client_host, socket_rfid_client_port))
        rfid_client_socket.listen(1)
        print("Ouvindo em", socket_rfid_client_host, "porta", socket_rfid_client_port)

        aceitar_conexoes(rfid_client_socket)

    except socket.error as e:
        print("Erro de conexão:", e)
    finally:
        rfid_client_socket.close()

if __name__ == "__main__":
    main()