import socket
import sys
import os
import json
import threading

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config import socket_host, socket_port, socket_rfid_client_host, socket_rfid_client_port


def menu():
    continuar = True

    while continuar:
        print('\n\n-=-=-=-= MENU ADMIN =-=-=-=-')
        print('[1] -> Ver informações sobre os caixas')
        print('[2] -> Bloquear/Liberar um caixa')
        print('[3] -> Histórico de compras')
        print('[4] -> Acompanhar compras em tempo real')
        print('[5] -> Sair')

        escolha = input('\nOpção -> ')

        if (escolha == '1'):
            print("Opção 1")
        elif (escolha == '2'):
            print("Opção 2")
        elif (escolha == '3'):
            print("Opção 3")
        elif (escolha == '4'):
            print("Opção 4")
        elif (escolha == '5'):
            continuar = False
        else:
            print('\nOpção inválida!')

def main():
    menu()
    

if __name__ == "__main__":
    main()