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

caixas = {'caixa1': {'socket': 'OBJSOCKET', 'ativo': True, 'bloqueado': False},
    'caixa2': {'socket': 'OBJSOCKET', 'ativo': True, 'bloqueado': True},
    'caixa3': {'socket': 'OBJSOCKET', 'ativo': False, 'bloqueado': False},
    'caixa4': {'socket': 'OBJSOCKET', 'ativo': True, 'bloqueado': False}
}

body = {
    'caixa1': {'socket': '1', 'ativo': 2}
}

print(caixas['caixa1'])

for caixa, info_atualizada in body.items():
    if caixa in caixas:
        caixas[caixa].update(info_atualizada)

print(caixas['caixa1'])
