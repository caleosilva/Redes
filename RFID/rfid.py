import socket
import mercury
import time

# Configuração do leitor
reader = mercury.Reader("tmr:///COM1")  # Substitua "COM1" pela porta do seu leitor, "tmr://192.168.1.101"

# Inicialização do leitor
reader.connect()

# Configuração do socket
HOST = 'destino'
PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Dicionário para armazenar o último tempo de leitura de cada tag
ultimo_tempo_leitura = {}

try:
    # Leitura e envio das tags em tempo real
    while True:
        tags = reader.read()  # Leitura de tags
        for tag in tags:
            tag_id = tag.epc

            # Verifica se a tag já foi lida recentemente
            tempo_atual = time.time()
            if tag_id not in ultimo_tempo_leitura or (tempo_atual - ultimo_tempo_leitura[tag_id]) > 2.0:  # Aguarda 2 segundos
                ultimo_tempo_leitura[tag_id] = tempo_atual
                sock.send(tag_id.encode())
                response = sock.recv(1024)  # Aguarda resposta do destino
                print("Resposta do destino:", response.decode())

except KeyboardInterrupt:
    print("Leitura interrompida pelo usuário")

finally:
    sock.close()
    reader.stop_reading()  # Parar a leitura do leitor antes de fechar
    reader.disconnect()    # Desconectar o leitor
