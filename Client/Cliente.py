import requests

while True:
    id = input(" -> ")
    r = requests.get('http://localhost:8000/' + id)

    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if r.status_code == 200:
        # Decodifica o conteúdo da resposta usando UTF-8 e imprime
        print(r.text)
    else:
        print("Erro:", r.status_code)
