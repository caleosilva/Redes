import socket
import sys
import os
import json
import threading

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port, socket_rfid_client_host, socket_rfid_client_port

carrinho = {
    '1': {"nome": "Whey", "preco": 1.99, "quantidade": 1},
    '2': {"nome": "A", "preco": 1.99, "quantidade": 2},
    '3': {"nome": "B", "preco": 1.99, "quantidade": 3}
}

def enviar_carrinho(client_server_socket, data):
    serialized_data = json.dumps(data)
    data_size = len(serialized_data)
    client_server_socket.send(str(data_size).encode())  # Envia o tamanho dos dados

    ack = client_server_socket.recv(1024)  # Espera por um ack do servidor
    if ack.decode() == 'OK':
        sent_bytes = 0
        while sent_bytes < data_size:
            remaining_data = serialized_data[sent_bytes:]
            bytes_to_send = min(1024, data_size - sent_bytes)
            client_server_socket.send(remaining_data[:bytes_to_send].encode())
            sent_bytes += bytes_to_send

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

def adicionar_produto_carrinho(produto):
    if (produto == "204"):
        pass
    else:
        data_dict = json.loads(produto)
        for chave, valor in data_dict.items():
            if chave in carrinho:
                carrinho[chave]['quantidade'] += 1
            else:
                carrinho[chave] = valor
                carrinho[chave]['quantidade'] = 1

def comunicacao_socket(rfid_socket, client_server_socket):
    try:
        while True:
            dados_recebidos = rfid_socket.recv(1024).decode()
            data = json.loads(dados_recebidos)

            if data:
                if (data['header'] == 'comprar'):
                    data['body'] = carrinho
                    enviar_carrinho(client_server_socket, data)
                    rfid_socket.send('compra finalizada'.encode('utf-8'))
                elif (data['header'] == 'id'):
                    produtoInfo = solicitar_info_produto(client_server_socket, data)
                    adicionar_produto_carrinho(produtoInfo)
                    rfid_socket.send(produtoInfo.encode('utf-8'))

            mostrarCarrinho()
    except socket.error as e:
        print("Erro de soquete:", e)
        rfid_socket.close()  # Fechar o socket em caso de erro
        client_server_socket.close()  # Fechar o socket em caso de erro
    except KeyboardInterrupt:
        print("Cliente interrompido pelo usuário.")
        rfid_socket.close()  # Fechar o socket em caso de interrupção
        client_server_socket.close()

def solicitar_info_produto(client_server_socket, data):
    serialized_data = json.dumps(data)
    data_size = len(serialized_data)
    client_server_socket.send(str(data_size).encode())  # Envia o tamanho dos dados

    ack = client_server_socket.recv(1024)  # Espera por um ack do servidor
    if ack.decode() == 'OK':
        sent_bytes = 0
        while sent_bytes < data_size:
            remaining_data = serialized_data[sent_bytes:]
            bytes_to_send = min(1024, data_size - sent_bytes)
            client_server_socket.send(remaining_data[:bytes_to_send].encode())
            sent_bytes += bytes_to_send

    return client_server_socket.recv(1024).decode('utf-8')

# def solicitar_produto_id(client_server_socket, data, rfid_socket):
#     data_serialized = json.dumps(data)  # Serializa o dicionário em JSON
#     client_server_socket.send(data_serialized.encode())  # Envia os dados serializados
#     dataRcv = client_server_socket.recv(1024).decode('utf-8')
#     rfid_socket.send(dataRcv.encode('utf-8'))

#     if (dataRcv == "204"):
#         pass
#     else:
#         data_dict = json.loads(dataRcv)
#         for chave, valor in data_dict.items():
#             if chave in carrinho:
#                 carrinho[chave]['quantidade'] += 1
#             else:
#                 carrinho[chave] = valor
#                 carrinho[chave]['quantidade'] = 1


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