import socket
import sys
import json
import mercury


def aceitar_conexoes(rfid_client_socket):
    while True:
        rfid_socket, rfid_address = rfid_client_socket.accept()
        print("Conexão iniciada com:", rfid_address)
        comunicacao_socket(rfid_socket)

def comunicacao_socket(rfid_client_socket):
    try:
        # Configs:
        param = 2300
        if len(sys.argv) > 1:
                param = int(sys.argv[1])
        reader = mercury.Reader("tmr:///dev/ttyUSB0")
        reader.set_region("NA2")
        reader.set_read_plan([1], "GEN2", read_power=param)

        listaFormatadaTAGS = []
        epcs = map(lambda tag: tag, reader.read())
        for tag in epcs:
            encoded_id = (tag.epc).decode()
            listaFormatadaTAGS.append(encoded_id)
        
        # print(listaFormatadaTAGS)
        serialized_data = json.dumps(listaFormatadaTAGS)
        print(serialized_data)
        rfid_client_socket.send(serialized_data.encode())

        rfid_client_socket.close()
        print("Conexão finalizada com:", rfid_client_socket)

    except socket.error as e:
        print("Erro de soquete:", e)


def main():
    socket_rfid_client_host = '172.16.103.0'
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