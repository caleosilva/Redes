import socket
import sys
import json
from datetime import datetime
# import mercury


def comunicacao_socket(rfid_client_socket):
    try:
        enviarListaIdFalsa(rfid_client_socket)
    except socket.error as e:
        print("Erro de soquete:", e)
    except KeyboardInterrupt:
        print("RFID interrompido pelo usuário.")
    finally:
        print("Comunicação fechada")
        rfid_client_socket.close()


# def enviarId(rfid_client_socket):   
#     param = 2300

#     if len(sys.argv) > 1:
#             param = int(sys.argv[1])

#     # configura a leitura na porta serial onde esta o sensor
#     reader = mercury.Reader("tmr:///dev/ttyUSB0")

#     # para funcionar use sempre a regiao "NA2" (Americas)
#     reader.set_region("NA2")

#     # nao altere a potencia do sinal para nao prejudicar a placa
#     reader.set_read_plan([1], "GEN2", read_power=param)

#     # realiza a leitura das TAGs proximas e imprime na tela
#     # print(reader.read())

#     epcs = map(lambda tag: tag, reader.read())
#     # rfid_client_socket.send(epcs.encode())
#     for tag in epcs:
#         rfid_client_socket.send((tag.epc).encode())
#         confirmacao = rfid_client_socket.recv(1024).decode()
#         print(confirmacao)

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
    # host = '172.16.103.6'
    # port = 3430
    socket_rfid_client_host = '127.0.0.1'
    socket_rfid_client_port = 1234

    rfid_client_socket = socket.socket()

    try:
        rfid_client_socket.connect((socket_rfid_client_host, socket_rfid_client_port))
        print("Conectado ao rfid_client_socket em", socket_rfid_client_host, "porta", socket_rfid_client_port)
        comunicacao_socket(rfid_client_socket)
    except socket.error as e:
        print("Erro de conexão:", e)
    finally:
        rfid_client_socket.close()

if __name__ == "__main__":
    main()