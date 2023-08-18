import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import socket
import threading
import queue
import requests
from config import server_host, socket_host, socket_port



def client_handler(server_socket, data_queue):
    while True:
        client_socket, client_address = server_socket.accept()
        try:
            id = client_socket.recv(1024).decode('utf-8')
            data_queue.put((id, client_socket))
        except Exception as e:
            print("Erro client_handler:", e)

def process_data(id, conn):
    r = requests.get(server_host + id)
    
    if r.status_code == 200:
        response_text = r.text
        conn.send(response_text.encode('utf-8'))
    else:
        error_message = "Erro na requisição"
        conn.send(error_message.encode('utf-8'))


def worker(data_queue):
    try:
        while True:
            id, conn = data_queue.get()
            process_data(id, conn)
            # conn.close()
            data_queue.task_done()
    except Exception as e:
        print("Erro no worker:", e)
    finally:
        conn.close()

def main():
    host = socket_host
    port = socket_port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Socket ouvindo em", host, "porta", port)


    data_queue = queue.Queue()

    # Inicia a thread para receber IDs
    client_thread = threading.Thread(target=client_handler, args=(server_socket, data_queue))
    client_thread.start()

    # Inicia as threads para processar IDs
    num_workers = 4  # Número de threads de processamento
    for _ in range(num_workers):
        worker_thread = threading.Thread(target=worker, args=(data_queue,)) # responsável por processar os IDs a partir da fila
        worker_thread.daemon = True # Se a Thread principal encerrar, todas as paralelas também irão.
        worker_thread.start()

    # Aguarda a conclusão das threads
    client_thread.join()
    data_queue.join()

if __name__ == "__main__":
    main()