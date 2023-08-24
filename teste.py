import socket
import sys
import json
from datetime import datetime
import mercury


def comunicacao_socket(client_socket):
    try:
        while True:
            message = input("-> ")
            if (message):
                enviarID_receberProduto(client_socket)
    except socket.error as e:
        print("Erro de soquete:", e)
    except KeyboardInterrupt:
        print("Cliente interrompido pelo usuário.")
    finally:
        print("Fechei a comunicação")
        client_socket.close()


def enviarID_receberProduto(client_socket):   
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
    # client_socket.send(epcs.encode())
    for tag in epcs:
        client_socket.send((tag.epc).encode())
    

def main():
    host = '172.16.103.6'
    port = 3430

    client_socket = socket.socket()

    try:
        client_socket.connect((host, port))
        print("Conectado ao socket em", host, "porta", port)
        comunicacao_socket(client_socket)
    except socket.error as e:
        print("Erro de conexão:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()