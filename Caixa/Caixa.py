import socket
import sys
import os
import json
import threading

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port, socket_rfid_client_host, socket_rfid_client_port

carrinho = {
    '1': {"nome": "Whey", "preco": 1.99, "quantidade": 1}
}

def mostrarCarrinho():
    os.system('clear')
    totalItens = len(carrinho)
    valorTotal = 0
    if(totalItens > 0):
        print('-=-=-= Carrinho =-=-=-')
        for chave, valor in carrinho.items():
            print(f"[{chave}] {valor['nome']} (R$ {valor['preco']}): {valor['quantidade']} unidades")
            # print(valor['preco'])
            valorTotal += valor['preco'] * valor['quantidade']
        print(f"\nPreço total: R$ {valorTotal:.2f}")
    else:
        print("O carrinho está vazio.")
    print('\n\n')

def comunicacao_socket(rfid_socket, client_server_socket):
    try:
        while True:
            dados_recebidos = rfid_socket.recv(1024).decode()
            data = json.loads(dados_recebidos)

            if data:
                if (data['header'] == 'comprar'):
                    rfid_socket.send('compra finalizada'.encode('utf-8'))
                elif (data['header'] == 'id'):
                    enviarID_receberProduto(client_server_socket, data, rfid_socket)
            mostrarCarrinho()
    except socket.error as e:
        print("Erro de soquete:", e)
        rfid_socket.close()  # Fechar o socket em caso de erro
        client_server_socket.close()  # Fechar o socket em caso de erro
    except KeyboardInterrupt:
        print("Cliente interrompido pelo usuário.")
        rfid_socket.close()  # Fechar o socket em caso de interrupção
        client_server_socket.close()


def enviarID_receberProduto(client_server_socket, data, rfid_socket):
    data_serialized = json.dumps(data)  # Serializa o dicionário em JSON
    client_server_socket.send(data_serialized.encode())  # Envia os dados serializados
    dataRcv = client_server_socket.recv(1024).decode('utf-8')
    rfid_socket.send(dataRcv.encode('utf-8'))

    if (dataRcv == "204"):
        pass
    else:
        data_dict = json.loads(dataRcv)
        for chave, valor in data_dict.items():
            if chave in carrinho:
                carrinho[chave]['quantidade'] += 1
            else:
                carrinho[chave] = valor
                carrinho[chave]['quantidade'] = 1



def main():
    rfid_client_socket = socket.socket()
    client_server_socket = socket.socket()

    try:
        client_server_socket.connect((socket_host, socket_port))
        rfid_client_socket.connect((socket_rfid_client_host, socket_rfid_client_port))

        print("Conectado ao rfid_client_socket em", socket_rfid_client_host, "porta", socket_rfid_client_port)
        print("Conectado ao client_server_socket em", socket_host, "porta", socket_port)

        accept_thread = threading.Thread(target=comunicacao_socket, args=(rfid_client_socket, client_server_socket))
        accept_thread.start()
    except socket.error as e:
        print("Erro de conexão:", e)
    

if __name__ == "__main__":
    main()