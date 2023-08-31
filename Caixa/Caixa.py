import socket
import sys
import os
import json
import threading

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port, socket_rfid_client_host, socket_rfid_client_port

carrinho = {
    '5': {"nome": "Batata", "preco": 6.99, "quantidade": 5}
}

def send_receive_data(socket, data):
    serialized_data = json.dumps(data)
    data_size = len(serialized_data)
    
    socket.send(str(data_size).encode())  # Envia o tamanho dos dados
    
    ack = socket.recv(1024)  # Espera por um ack do servidor
    if ack.decode() == 'OK':
        socket.sendall(serialized_data.encode())
        return socket.recv(1024).decode('utf-8')

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
            if (valor['quantidade'] > 0):
                if (chave in carrinho and carrinho[chave]['quantidade'] < valor['quantidade']):
                    carrinho[chave]['quantidade'] += 1
                elif (chave not in carrinho):
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
                    data = send_receive_data(client_server_socket, data)
                    rfid_socket.send('compra finalizada'.encode('utf-8'))
                elif (data['header'] == 'id'):
                    produtoInfo = send_receive_data(client_server_socket, data)

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