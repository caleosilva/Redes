import socket
import json


def aceitar_conexoes(rfid_client_socket):
    while True:
        rfid_socket, rfid_address = rfid_client_socket.accept()
        print("Conexão iniciada com:", rfid_address)
        comunicacao_socket(rfid_socket, rfid_address)

def comunicacao_socket(rfid_client_socket, rfid_address):
    try:
        listaFormatadaTAGS = [
            "E2000017221100961890544A",
            "E20000172211009418905449",
            "E20000172211012518905484",
            "E20000172211011118905471",
            "E20000172211010118905454",
            "E20000172211010218905459",
            "E2000017221101241890547C",
            "E20000172211011718905474",
            "E2000017221101321890548C"
        ]
        serialized_data = json.dumps(listaFormatadaTAGS)
        rfid_client_socket.send(serialized_data.encode())
        rfid_client_socket.close()
        print("Conexão finalizada com:", rfid_address)

    except socket.error as e:
        print("Erro de soquete:", e)


def main():
    # socket_rfid_client_host = '172.16.103.0'
    socket_rfid_client_host = '127.0.0.1'
    socket_rfid_client_port = 3983
    try:
        rfid_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rfid_client_socket.bind((socket_rfid_client_host, socket_rfid_client_port))
        rfid_client_socket.listen(1)
        print("Ouvindo em", socket_rfid_client_host, "porta", socket_rfid_client_port)

        aceitar_conexoes(rfid_client_socket)
    except socket.error as e:
        print("Erro de conexão:", e)
    finally:
        rfid_client_socket.close()

if __name__ == "__main__":
    main()