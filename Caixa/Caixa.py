import socket
import sys
import os
import json
import threading

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port, socket_rfid_client_host, socket_rfid_client_port

carrinho = {}

def enviar_ID_manualmente(client_server_socket):
    inputData = input('ID -> ')

    if (inputData == ''):
        print("ID inválido!\n")
    else:
        inputDataDict = {'header':'id', 'body': inputData}
        dataRcv = send_receive_data(client_server_socket, inputDataDict)
        return dataRcv

def send_receive_data(socket, data):
    serialized_data = json.dumps(data)
    data_size = len(serialized_data)
    
    socket.send(str(data_size).encode())  # Envia o tamanho dos dados
    
    ack = socket.recv(1024)  # Espera por um ack do servidor
    if ack.decode() == 'OK':
        socket.sendall(serialized_data.encode())
        return socket.recv(1024).decode('utf-8')

def mostrarCarrinho():
    totalItens = len(carrinho)
    valorTotal = 0
    if(totalItens > 0):
        print('\n-=-=-= CARRINHO =-=-=-')
        for chave, valor in carrinho.items():
            print(f"[{chave}] {valor['nome']} (R$ {valor['preco']}): {valor['quantidade']} unidades")
            # print(valor['preco'])
            valorTotal += valor['preco'] * valor['quantidade']
        print(f"\nPreço total: R$ {valorTotal:.2f}")
    else:
        print("\nO carrinho está vazio.")

def adicionar_produto_carrinho(produto):
    if (produto == "204"):
        pass
    else:
        data_dict = json.loads(produto)
        for chave, valor in data_dict.items():
            if (valor['quantidade'] > 0):
                if (chave in carrinho and carrinho[chave]['quantidade'] < valor['quantidade']):
                    carrinho[chave]['quantidade'] += 1
                    print(f"\nO produto '{valor['nome']}' foi adicionado ao carrinho.")
                elif (chave not in carrinho):
                    carrinho[chave] = valor
                    carrinho[chave]['quantidade'] = 1
                    print(f"\nO produto '{valor['nome']}' foi adicionado ao carrinho.")

            else:
                print(f'\nO produto {valor["nome"]} não tem estoque!')

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

def solicitar_tags_RFID():
    try:
        rfid_caixa_socket = socket.socket()
        rfid_caixa_socket.connect((socket_rfid_client_host, socket_rfid_client_port))
        dadosRcv = rfid_caixa_socket.recv(1024).decode()
        return json.loads(dadosRcv)
    except socket.error as e:
        print("\nNão foi possível se conectar com o RFID.")

def menu(client_server_socket):
    continuar = True

    while continuar:
        print('\n\n-=-=-=-= MENU =-=-=-=-')
        print('[1] -> Inserir código manualmente')
        print('[2] -> Ler RFID')
        print('[3] -> Visualizar carrinho')
        print('[4] -> Finalizar compra')

        escolha = input('\nOpção -> ')

        if (escolha == '1'):
            produtoID = enviar_ID_manualmente(client_server_socket)
            adicionar_produto_carrinho(produtoID)
        elif (escolha == '2'):
            listaRFID = solicitar_tags_RFID()
            if(len(listaRFID) > 0):
                for id in listaRFID:
                    inputDataDict = {'header':'id', 'body': id}
                    dataRcv = send_receive_data(client_server_socket, inputDataDict)
                    adicionar_produto_carrinho(dataRcv)
        elif (escolha == '3'):
            mostrarCarrinho()
        elif (escolha == '4'):
            print('4')
        else:
            print('Opção inválida!')

def main():
    caixa_controller_socket = socket.socket()

    try:
        caixa_controller_socket.connect((socket_host, socket_port))
        print("Conectado ao caixa_controller_socket em", socket_host, "porta", socket_port)

        accept_thread = threading.Thread(target=menu, args=(caixa_controller_socket,))
        accept_thread.start()
    except socket.error as e:
        print("Erro de conexão:", e)
    

if __name__ == "__main__":
    main()