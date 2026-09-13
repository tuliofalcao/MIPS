import json
from decodificador import decodificador
from instrucoesMips import get_instrucao_mips

def main():
    # =========================================================================
    # 1. LEITURA E TRATAMENTO DA ENTRADA
    # =========================================================================
    # Chama a função do módulo decodificador.py para extrair a lista de instruções em hex do JSON
    instrucoes_hex = decodificador() 
    
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
    
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        # json.dump salva o dicionário no formato JSON com indentação legível (4 espaços)
        json.dump(resultado_json, f, indent=4)

    print(f"[Sucesso] Processamento concluído! {len(resultado_json)} instruções decodificadas.")
    print(f"[Arquivo Gerado]: '{nome_arquivo_saida}'")


if __name__ == "__main__":
    main()
