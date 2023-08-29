import socket
import sys
import os
import json
import threading

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port, socket_rfid_client_host, socket_rfid_client_port

carrinho = {
    "2": {"nome": "Melancia", "preco": 8.99, "quantidade": 1},
    "5": {"nome": "Banana", "preco": 1.99, "quantidade": 1},
    "7": {"nome": "Uva", "preco": 5.99, "quantidade": 1},
    "3": {"nome": "Abobora", "preco": 4.99, "quantidade": 1},
    "8": {"nome": "Pera", "preco": 2.99, "quantidade": 1},
    "9": {"nome": "Kiwi", "preco": 6.99, "quantidade": 1},
    "1": {"nome": "Abacaxi", "preco": 10.99, "quantidade": 1},
    "10": {"nome": "Manga", "preco": 4.49, "quantidade": 1}
}

def aceitarConexao(rfid_server_socket, client_server_socket):
    while True:
        rfid_socket, rfid_address = rfid_server_socket.accept()
        print("Nova conexão:", rfid_address, "\n")

        # print("aceitarConexao", client_server_socket)


        comunicacao_socket(rfid_socket, client_server_socket)

        # print("aceitarConexao", client_server_socket)

        

def comunicacao_socket(rfid_socket, client_server_socket):
    try:
        while True:
            data = rfid_socket.recv(1024).decode()

            if data:
                # print("comunicacao_socket", rfid_socket)

                enviarID_receberProduto(client_server_socket, data)
                print(data)
                rfid_socket.send('ok'.encode())

            # message = input("-> ")
            # if (message):
            #     if (message == "comprar"):
            #         print("Compra finalizada - fazer função")
            #     elif (message == "ver"):
            #         for chave, valor in carrinho.items():
            #             print(f"[{chave}] {valor['nome']}: {valor['quantidade']}")
            #     else:
            #         continue
    except socket.error as e:
        print("Erro de soquete:", e)
        rfid_socket.close()  # Fechar o socket em caso de erro
        client_server_socket.close()  # Fechar o socket em caso de erro
    except KeyboardInterrupt:
        print("Cliente interrompido pelo usuário.")
        rfid_socket.close()  # Fechar o socket em caso de interrupção
        client_server_socket.close()


def enviarID_receberProduto(client_server_socket, data):

    client_server_socket.send(data.encode('utf-8'))
    dataRcv = client_server_socket.recv(1024).decode('utf-8')
    print("dataRcv", dataRcv)
    # if (dataRcv != "204"):
    #     data_dict = json.loads(dataRcv)

    #     if dataRcv in carrinho:
    #         carrinho[dataRcv]['quantidade'] += 1
    #     else:
    #         carrinho[dataRcv] = data_dict

    #     print(f"O produto '{data_dict[dataRcv]['nome']}' foi adicionado ao carrinho!")
    # else:
    #     print('Produto não encontrado')

def main():
    rfid_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rfid_server_socket.bind((socket_rfid_client_host, socket_rfid_client_port))
    rfid_server_socket.listen()

    client_server_socket = socket.socket()

    try:
        client_server_socket.connect((socket_host, socket_port))

        print("Conectado ao rfid_client_socket em", socket_rfid_client_host, "porta", socket_rfid_client_port)
        print("Conectado ao client_server_socket em", socket_host, "porta", socket_port)

        # print('\n main: ', client_server_socket, '\n')

        accept_thread = threading.Thread(target=aceitarConexao, args=(rfid_server_socket, client_server_socket))
        accept_thread.start()

    except socket.error as e:
        print("Erro de conexão:", e)
    

if __name__ == "__main__":
    main()