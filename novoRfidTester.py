import socket
import sys
import json
from datetime import datetime
import mercury
import time
import threading


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
    param = 2300

    if len(sys.argv) > 1:
            param = int(sys.argv[1])

    # configura a leitura na porta serial onde esta o sensor
    reader = mercury.Reader("tmr:///dev/ttyUSB0")

    # para funcionar use sempre a regiao "NA2" (Americas)
    reader.set_region("NA2")

    # nao altere a potencia do sinal para nao prejudicar a placa
    reader.set_read_plan([1], "GEN2", read_power=param)

    epcs = map(lambda tag: tag, reader.read())
    for tag in epcs:
        encoded_id = (tag.epc).decode()
        print(encoded_id)
        tempo_atual = time.time()
        if ((encoded_id not in ultimo_tempo_leitura) or (tempo_atual - ultimo_tempo_leitura[encoded_id]) > 5.0):
            ultimo_tempo_leitura[encoded_id] = tempo_atual

            rfid_client_socket.send(encoded_id.encode())
            confirmacao = rfid_client_socket.recv(1024).decode('utf-8')
            print('ok')


def main():
    socket_rfid_client_host = '172.16.103.0'
    socket_rfid_client_port = 1234

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