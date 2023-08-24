import socket
import sys
import os
import json

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port

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

def comunicacao_socket(client_socket):
    try:
        while True:
            message = input("-> ")
            if (message):
                if (message == "end"):
                    print("Compra finalizada - fazer função")
                elif (message == "ver"):
                    for chave, valor in carrinho.items():
                        print(f"[{chave}] {valor['nome']}: {valor['quantidade']}")
                else:
                    enviarID_receberProduto(client_socket, message)
    except socket.error as e:
        print("Erro de soquete:", e)
    except KeyboardInterrupt:
        print("Cliente interrompido pelo usuário.")
    finally:
        print("Fechei a comunicação")
        client_socket.close()


def enviarID_receberProduto(client_socket, id):   
    client_socket.send(id.encode())
    data = client_socket.recv(1024).decode()
    if (data != "204"):
        data_dict = json.loads(data)

        if id in carrinho:
            carrinho[id]['quantidade'] += 1
        else:
            carrinho[id] = data_dict

        print(f"O produto '{data_dict[id]['nome']}' foi adicionado ao carrinho!")
    else:
        print('Produto não encontrado')

def main():
    host = socket_host
    port = socket_port

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