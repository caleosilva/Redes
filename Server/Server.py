from http.server import BaseHTTPRequestHandler, HTTPServer
import json

dados = {
    "1": {"nome": "Abacaxi", "preco": "10.99", "quantidade": 10},
    "2": {"nome": "Melancia", "preco": "8.99", "quantidade": 5},
    "3": {"nome": "Abobora", "preco": "4.99", "quantidade": 23}
}


# Define uma classe de manipulador personalizada que herda de BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):
    # Método para lidar com solicitações GET
    def do_GET(self):
        # Envia uma resposta com código 200 (OK)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')  # "text/html"
        self.end_headers()

        partes_url = self.path.split('/')

        if partes_url[1] == '':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write (json.dumps(dados).encode('utf-8'))

        elif partes_url[1] != '' and len(partes_url) == 2:

            id_fruta = partes_url[1]

            # Verifica se o ID da fruta existe no dicionário de dados
            if id_fruta in dados:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(dados[id_fruta]).encode('utf-8'))


            else:
                self.send_response(204)
                self.end_headers()
                self.wfile.write(b'Fruta nao encontrada')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'URL invalida')

    # Método para lidar com solicitações POST

    def do_POST(self):
        # Envia uma resposta com código 200 (OK)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        # Lê os dados do corpo da solicitação POST
        post_data = self.rfile.read(content_length)
        # Escreve a resposta no corpo da mensagem, incluindo os dados POST recebidos
        self.wfile.write(b'Hello, POST! You sent: ' + post_data)

# Função para executar o servidor


def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    # Inicia o servidor e o faz rodar indefinidamente
    httpd.serve_forever()


# Executa o servidor se este script for executado diretamente
if __name__ == '__main__':
    run()
