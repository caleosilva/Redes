dados = {
    '1': {"nome": "Whey", "preco": 1.99, "quantidade": 0},
    '2': {"nome": "Creatina", "preco": 3.99, "quantidade": 10},
    '3': {"nome": "HiperCalorico", "preco": 5.99, "quantidade": 10},
    '4': {"nome": "Ovo", "preco": 2.99, "quantidade": 20},
    '5': {"nome": "Batata", "preco": 6.99, "quantidade": 20}
}

carrinho = {
    '2': {'nome': 'Creatina', 'preco': 3.99, 'quantidade': 1},
    '3': {"nome": "HiperCalorico", "preco": 5.99, "quantidade": 1},
    '4': {"nome": "Ovo", "preco": 2.99, "quantidade": 2},
    '5': {"nome": "Batata", "preco": 6.99, "quantidade": 2}
}


for chave, valor in carrinho.items():
    if (dados[chave]['quantidade'] >= valor['quantidade']):
        dados[chave]['quantidade'] -= valor['quantidade']

for chave, valor in dados.items():
    print(valor)
