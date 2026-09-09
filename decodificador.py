import json


def decodificador():
    with open('entrada.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
        
    return dados['text']
    
    