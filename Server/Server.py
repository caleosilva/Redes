from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from dadosDict import dados
from caixas import caixas
from comprasEmAndamento import comprasEmAndamento


lock = threading.Lock()
# Define uma classe de manipulador personalizada que herda de BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        partes_url = self.path.split('/')
        
        # Busca por produto
        if (partes_url[1] == 'id' and len(partes_url) == 2):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dados).encode('utf-8'))
        elif (partes_url[1] == 'id' and len(partes_url) == 3):
            id_produto = partes_url[2]
            
            if id_produto in dados:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({id_produto: dados[id_produto]}).encode('utf-8'))
            else:
                self.send_response(204)
                self.end_headers()
                self.wfile.write(b'Produto nao encontrada')
        
        # Busca por caixas
        elif (partes_url[1] == 'caixas' and len(partes_url) == 2):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(caixas).encode('utf-8'))
        elif (partes_url[1] == 'caixas' and len(partes_url) == 3):
            id_caixa = partes_url[2]

            if id_caixa in caixas:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({id_caixa: caixas[id_caixa]}).encode('utf-8'))
            else:
                self.send_response(204)
                self.end_headers()
                self.wfile.write(b'Caixa nao encontrada')

        elif (partes_url[1] == 'produtosCaixa' and len(partes_url) == 2):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(comprasEmAndamento).encode('utf-8'))
        
        elif (partes_url[1] == 'produtosCaixa' and partes_url[2] != '' and len(partes_url) == 3):
            idCaixa = partes_url[2]

            if (idCaixa in comprasEmAndamento):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(comprasEmAndamento[idCaixa]).encode('utf-8'))
            else:
                self.send_response(204)
                self.end_headers()
                self.wfile.write(b'Caixa nao encontrado')
        
        
        
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'URL invalida')

    def do_POST(self):
        partes_url = self.path.split('/')
        content_length = int(self.headers['Content-Length'])
        dadosBody = self.rfile.read(content_length)
        dadosBodyStr = dadosBody.decode()
                    
        try:
            dadosJson = json.loads(dadosBodyStr)
        except json.JSONDecodeError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Erro no formato JSON."}).encode())
            return
        
        # Realizar compra
        if (partes_url[1] == 'comprar' and partes_url[2] != '' and len(partes_url) == 3):
            dadosTirados = []
            idCaixa = partes_url[2]

            with lock:
                for produto in dadosJson:
                    chave = produto['chave']
                    valor = produto['quantidade']
                    if chave in dados and dados[chave]['quantidade'] >= valor:
                        dados[chave]['quantidade'] -= valor
                        dadosTirados.append({"chave": chave, "quantidade": valor})
                    else:
                        for prod in dadosTirados:
                            chave = prod['chave']
                            valor = prod['quantidade']
                            dados[chave]['quantidade'] += valor
                        
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": "Produto não disponível em quantidade suficiente."}).encode())
                        return
                
                caixas[partes_url[2]]['historicoCompras'].append(dadosJson)
                comprasEmAndamento[partes_url[2]].clear()

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"statusCompra": "Compra finalizada com sucesso."}).encode())
        
        # Manipular caixa
        elif (partes_url[1] == 'gerenciarCaixa' and len(partes_url) == 3):
            id_caixa = partes_url[2]
            with lock:
                if id_caixa in caixas:
                    caixas[id_caixa].update(dadosJson)
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"statusAtualizacao": "Atualizacao finalizada com sucesso."}).encode())
                    return
                else:
                    self.send_response(204)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"statusAtualizacao": "Caixa não encontrado"}).encode())
                    return                
        
        # Adicionar um produto no caixa
        elif (partes_url[1] == 'adicionarProdutoCaixa' and partes_url[2] != '' and len(partes_url) == 3):
            idCaixa = partes_url[2]
            if (idCaixa in comprasEmAndamento):
                comprasEmAndamento[idCaixa].append(dadosJson)

                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "Produto adicionado ao carrinho"}).encode())
            else:
                self.send_response(204)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "Caixa não encontrado"}).encode())
        
        elif (partes_url[1] == 'limparCarrinho' and partes_url[2] != '' and len(partes_url) == 3):
            idCaixa = partes_url[2]
            
            if (idCaixa in comprasEmAndamento):
                comprasEmAndamento[idCaixa].clear()

                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "Carrinho limpado"}).encode())
            else:
                self.send_response(204)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "Caixa não encontrado"}).encode())

        # URL incorreta
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint não encontrado."}).encode())



def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


# Executa o servidor se este script for executado diretamente
if __name__ == '__main__':
    run()