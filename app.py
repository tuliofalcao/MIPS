import json
from decodificador import decodificador
from instrucoesMips import get_instrucao_mips
from banco_registradores import BancoRegistradores
from executor import executar_instrucao

def main():
    # =========================================================================
    # 1. LEITURA E TRATAMENTO DA ENTRADA
    # =========================================================================
    # Chama a função do módulo decodificador.py para extrair os dados do arquivo JSON
    dados = decodificador()

    # Extrai a lista de instruções em hexadecimal do JSON
    instrucoes_hex = dados["text"]

    # Extrai as configurações iniciais dos registradores, caso existam
    config = dados.get("config", {})

    instrucoes_binarias = []
    
    # Valida e converte cada instrução Hexadecimal para uma string Binária de 32 bits
    for instrucao in instrucoes_hex:
        # Garante que a instrução inicia com '0x' ou '0X'
        if instrucao.lower().startswith("0x"):
            # Converte Hexadecimal para Inteiro -> Inteiro para Binário (removendo o prefixo '0b')
            # zfill(32) garante que a string binária tenha exatamente 32 bits (preenche zeros à esquerda)
            instrucao_binaria = bin(int(instrucao, 16))[2:].zfill(32)
            instrucoes_binarias.append(instrucao_binaria)
        else:
            print(f"Erro: A instrução '{instrucao}' não está no formato hexadecimal válido.")

    # Inicializa o banco de registradores com os valores configurados na entrada
    banco = BancoRegistradores(config)

    # =========================================================================
    # 2. DESMONTAGEM (DISASSEMBLY) DAS INSTRUÇÕES
    # =========================================================================
    # Envia a lista de strings binárias para a lógica central em instrucoesMips.py
    # O retorno é a lista de instruções formatadas em Assembly MIPS
    codigo_desmontado = get_instrucao_mips(instrucoes_binarias)

    # =========================================================================
    # 3. MONTAGEM DA ESTRUTURA DE SAÍDA EXIGIDA PELO PROJETO
    # =========================================================================
    # A especificação exige que a saída seja uma lista de objetos JSON contendo:
    # hex, text, regs, mem e stdout.
    resultado_json = []

    for hex_val, asm_text in zip(instrucoes_hex, codigo_desmontado):
        objeto_instrucao = {
            "hex": hex_val,
            "text": asm_text,
            "regs": {},    # Na Etapa 1, permanece um objeto vazio
            "mem": {},     # Na Etapa 1, permanece um objeto vazio
            "stdout": {}   # Na Etapa 1, permanece um objeto vazio
        }
        resultado_json.append(objeto_instrucao)

    # =========================================================================
    # 4. GERAÇÃO DO ARQUIVO DE SAÍDA JSON
    # =========================================================================
    nome_arquivo_saida = "saida.json"
    
    # Executa cada instrução e registra o estado dos registradores após sua execução
    resultado_json = []

    for hex_val, binario, asm_text in zip(
        instrucoes_hex,
        instrucoes_binarias,
        codigo_desmontado
    ):

        # Executa a instrução utilizando o banco de registradores
        executar_instrucao(binario, banco)

        # Obtém os registradores que possuem valores diferentes de zero
        registradores_atualizados = banco.exportar_para_json()

        objeto_instrucao = {
            "hex": hex_val,
            "text": asm_text,
            "regs": registradores_atualizados,
            "mem": {},     # A memória ainda não é utilizada nesta etapa
            "stdout": {}   # A saída padrão ainda não é utilizada nesta etapa
        }

        resultado_json.append(objeto_instrucao)

    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        # json.dump salva o dicionário no formato JSON com indentação legível (4 espaços)
        json.dump(resultado_json, f, indent=4)

    print(f"[Sucesso] Processamento concluído! {len(resultado_json)} instruções executadas.")
    print(f"[Arquivo Gerado]: '{nome_arquivo_saida}'")

if __name__ == "__main__":
    main()