import socket
import sys
import json
from datetime import datetime
import mercury
import time
import threading


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

    # realiza a leitura das TAGs proximas e imprime na tela
    # print(reader.read())

    epcs = map(lambda tag: tag, reader.read())
    for tag in epcs:
        encoded_id = (tag.epc).decode()
        print(encoded_id)
        tempo_atual = time.time()
        if ((encoded_id not in ultimo_tempo_leitura) or (tempo_atual - ultimo_tempo_leitura[encoded_id]) > 5.0):
            ultimo_tempo_leitura[encoded_id] = tempo_atual

            rfid_client_socket.send(encoded_id.encode())
            confirmacao = rfid_client_socket.recv(1024).decode('utf-8')
            print(confirmacao)

        

        # rfid_client_socket.send(tag.epc)
        # confirmacao = rfid_client_socket.recv(1024).decode('utf-8')
        # print(confirmacao)


        # stringTag = (tag.epc).decode("utf-8")

        # rfid_client_socket.send(stringTag.encode('utf-8'))
        # confirmacao = rfid_client_socket.recv(1024).decode('utf-8')
        # print(confirmacao)

def enviarListaIdFalsa(rfid_client_socket):   
    contador = 0
    lista = []

    while True:
        if contador == 0:
            contador += 1
            lista = [1, 2, 3, 4, 5]
        
        if(len(lista) > 0):
            for tag in lista:
                rfid_client_socket.send(str(tag).encode())
                confirmacao = rfid_client_socket.recv(1024).decode()
                print(confirmacao)
            lista = []
        
   

def main():

    socket_rfid_client_host = '172.16.103.6'
    socket_rfid_client_port = 1234
    

    # rfid_client_socket = socket.socket()

    try:
        rfid_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rfid_client_socket.bind((socket_rfid_client_host, socket_rfid_client_port))
        rfid_client_socket.listen(1)
        print("Ouvindo em", socket_rfid_client_host, "porta", socket_rfid_client_port)


        while True:
            rfid_socket, rfid_address = rfid_client_socket.accept()

            
            # rfid_client_socket.connect((socket_rfid_client_host, socket_rfid_client_port))
            # print("Conectado ao rfid_client_socket em", socket_rfid_client_host, "porta", socket_rfid_client_port)

            # if (rfid_socket):
            #     comunicacao_socket(rfid_client_socket)
            

    except socket.error as e:
        print("Erro de conexão:", e)
    finally:
        rfid_client_socket.close()

if __name__ == "__main__":
    main()