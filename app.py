from decodificador import decodificador
from instrucoesMips import get_instrucao_mips


#================ TRATAMENTO DA ENTRADA =====================

instrucoes = decodificador() # Extrai as instruções do arquivo JSON

instrucoesBinarias = []

for instrucao in instrucoes: # confere se as instruções estão no formato hexadecimal e as converte para binário
    if instrucao.startswith("0x"):
        instrucaoBinaria = bin(int(instrucao, 16))[2:].zfill(32)
        instrucoesBinarias.append(instrucaoBinaria)
    else:
        print(f"Erro: A instrução '{instrucao}' não está no formato hexadecimal.")
        
#================ DESASSEMBLE DAS INSTRUÇÕES =====================

codigo_desmontado = get_instrucao_mips(instrucoesBinarias) # Desmonta a instrução binária para o formato MIPS

print(codigo_desmontado)