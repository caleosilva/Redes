import mercury
import sys 
from datetime import datetime

import socket
 
HOST = '172.16.103.6' 
PORT = 3432
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = sock.connect((HOST, PORT))

param = 2300

if len(sys.argv) > 1:
        param = int(sys.argv[1])

# configura a leitura na porta serial onde esta o sensor
reader = mercury.Reader("tmr:///dev/ttyUSB0")

# para funcionar use sempre a regiao "NA2" (Americas)
reader.set_region("NA2")

# nao altere a potencia do sinal para nao prejudicar a placa
reader.set_read_plan([1], "GEN2", read_power=param)

# realiza a leitura das TAGs proximas e imprime na tela
# print(reader.read())

epcs = map(lambda tag: tag, reader.read())
client_socket.send(epcs.encode())
# for tag in epcs:
#         client_socket.send((tag.epc).encode())

