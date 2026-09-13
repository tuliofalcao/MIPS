import json
import os


def decodificador(caminho_arquivo: str = 'entrada.json') -> list:
    """
    Lê o arquivo JSON de entrada do simulador MIPS e extrai a lista 
    de instruções codificadas em hexadecimal.
    
    Parâmetros:
        caminho_arquivo (str): Caminho para o arquivo .json (padrão: 'entrada.json')
        
    Retorna:
        list: Lista contendo as strings em Hexadecimal (ex: ["0x02114020", ...])
    """
    # 1. Validação de segurança: verifica se o arquivo de entrada existe no diretório
    if not os.path.exists(caminho_arquivo):
        print(f"[Erro I/O] O arquivo de entrada '{caminho_arquivo}' não foi encontrado.")
        return []

    try:
        # 2. Abertura do arquivo JSON com garantia de suporte a caracteres UTF-8
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            # json.load faz o parse do conteúdo do arquivo para um dicionário Python
            dados = json.load(arquivo)
            
        # 3. Retorna a lista contida na chave "text" do JSON de entrada
        # O método .get() evita erros de KeyError caso a chave "text" não exista
        return dados.get('text', [])

    except json.JSONDecodeError:
        print(f"[Erro de Sintaxe] O arquivo '{caminho_arquivo}' não é um JSON válido.")
        return []
    except Exception as e:
        print(f"[Erro Inesperado] Falha ao processar o arquivo: {e}")
        return []
