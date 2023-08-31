from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from dadosDict import dados;


lock = threading.Lock()
# Define uma classe de manipulador personalizada que herda de BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):

    # Método para lidar com solicitações GET
    def do_GET(self):
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
                self.wfile.write(json.dumps({id_fruta: dados[id_fruta]}).encode('utf-8'))


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
        partes_url = self.path.split('/')
        content_length = int(self.headers['Content-Length'])
        dadosBody = self.rfile.read(content_length)
        
        print(dadosBody.decode())
        print(type(dadosBody.decode()))
        dadosJson = json.loads(dadosBody.decode())
        print(dadosJson)
        # dadosJson = json.dumps(dadosBody)
        # print(dadosJson)

        if partes_url[1] == 'comprar':
            with lock:
                for chave, valor in dadosJson.items():
                    if (dados[chave]['quantidade'] >= valor['quantidade']):
                        dados[chave]['quantidade'] -= valor['quantidade']
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"statusCompra": "Compra finalizada com sucesso."}))


def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    # Inicia o servidor e o faz rodar indefinidamente
    httpd.serve_forever()


# Executa o servidor se este script for executado diretamente
if __name__ == '__main__':
    run()