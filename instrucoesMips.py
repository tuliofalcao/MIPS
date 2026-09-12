# instrucoesMips.py

# ==============================================================================
# DICIONÁRIO COMPLETO DAS INSTRUÇÕES MIPS
# ==============================================================================
instrucoesMips = {
    # Tipo R
    "add":      {"tipo": 'r', "opcode": '000000', "funct": '100000'},
    "addu":     {"tipo": 'r', "opcode": '000000', "funct": '100001'},
    "sub":      {"tipo": 'r', "opcode": '000000', "funct": '100010'},
    "subu":     {"tipo": 'r', "opcode": '000000', "funct": '100011'},
    "and":      {"tipo": 'r', "opcode": '000000', "funct": '100100'},
    "or":       {"tipo": 'r', "opcode": '000000', "funct": '100101'},
    "xor":      {"tipo": 'r', "opcode": '000000', "funct": '100110'},
    "nor":      {"tipo": 'r', "opcode": '000000', "funct": '100111'},
    "slt":      {"tipo": 'r', "opcode": '000000', "funct": '101010'},
    "sll":      {"tipo": 'r', "opcode": '000000', "funct": '000000'},
    "srl":      {"tipo": 'r', "opcode": '000000', "funct": '000010'},
    "sra":      {"tipo": 'r', "opcode": '000000', "funct": '000011'},
    "sllv":     {"tipo": 'r', "opcode": '000000', "funct": '000100'},
    "srlv":     {"tipo": 'r', "opcode": '000000', "funct": '000110'},
    "srav":     {"tipo": 'r', "opcode": '000000', "funct": '000111'},
    "jr":       {"tipo": 'r', "opcode": '000000', "funct": '001000'},
    "mfhi":     {"tipo": 'r', "opcode": '000000', "funct": '010000'},
    "mflo":     {"tipo": 'r', "opcode": '000000', "funct": '010010'},
    "mult":     {"tipo": 'r', "opcode": '000000', "funct": '011008'},
    "multu":    {"tipo": 'r', "opcode": '000000', "funct": '011001'},
    "div":      {"tipo": 'r', "opcode": '000000', "funct": '011010'},
    "divu":     {"tipo": 'r', "opcode": '000000', "funct": '011011'},

    # Tipo I
    "addi":     {"tipo": 'i', "opcode": '001000', "funct": None},
    "addiu":    {"tipo": 'i', "opcode": '001001', "funct": None},
    "andi":     {"tipo": 'i', "opcode": '001100', "funct": None},
    "ori":      {"tipo": 'i', "opcode": '001101', "funct": None},
    "xori":     {"tipo": 'i', "opcode": '001110', "funct": None},
    "slti":     {"tipo": 'i', "opcode": '001010', "funct": None},
    "lui":      {"tipo": 'i', "opcode": '001111', "funct": None},
    "beq":      {"tipo": 'i', "opcode": '000100', "funct": None},
    "bne":      {"tipo": 'i', "opcode": '000101', "funct": None},
    "bgtz":     {"tipo": 'i', "opcode": '000111', "funct": None},
    "bltz":     {"tipo": 'i', "opcode": '000001', "funct": None},
    "blez":     {"tipo": 'i', "opcode": '000110', "funct": None},
    "lb":       {"tipo": 'i', "opcode": '100000', "funct": None},
    "lbu":      {"tipo": 'i', "opcode": '100100', "funct": None},
    "lw":       {"tipo": 'i', "opcode": '100011', "funct": None},
    "sb":       {"tipo": 'i', "opcode": '101000', "funct": None},
    "sw":       {"tipo": 'i', "opcode": '101011', "funct": None},

    # Tipo J
    "j":        {"tipo": 'j', "opcode": '000010', "funct": None},
    "jal":      {"tipo": 'j', "opcode": '000011', "funct": None},

    # Caso Especial
    "syscall":  {"tipo": None, "opcode": '000000', "funct": '001100'}
}


def get_instrucao_mips(instrucoesBinarias: list) -> list:
    """
    Decodifica palavras binárias de 32 bits para a sintaxe Assembly MIPS correspondente.
    """
    desassembled = []

    for binario in instrucoesBinarias:
        # Fatiamento dos campos binários
        opcode = binario[0:6]
        rs = int(binario[6:11], 2)
        rt = int(binario[11:16], 2)
        rd = int(binario[16:21], 2)
        shamt = int(binario[21:26], 2)
        funct = binario[26:32]

        immediate_bin = binario[16:32]
        address_bin = binario[6:32]

        instrucao_encontrada = None

        # Busca da instrução baseada no Opcode e Funct
        for nome, dados in instrucoesMips.items():
            if dados["tipo"] == "r" and opcode == dados["opcode"] and funct == dados["funct"]:
                instrucao_encontrada = nome
                break
            elif dados["tipo"] == "i" and opcode == dados["opcode"]:
                instrucao_encontrada = nome
                break
            elif dados["tipo"] == "j" and opcode == dados["opcode"]:
                instrucao_encontrada = nome
                break
            elif dados["tipo"] is None and opcode == dados["opcode"] and funct == dados["funct"]:
                instrucao_encontrada = nome
                break

        if instrucao_encontrada is None:
            desassembled.append(f"Instrução desconhecida: {binario}")
            continue

        nome = instrucao_encontrada
        tipo = instrucoesMips[nome]["tipo"]

        # ----------------------------------------------------------------------
        # VERIFICAÇÃO EXPLÍCITA DO SYSCALL (Evita queda nas checagens de Tipo R)
        # ----------------------------------------------------------------------
        if nome == "syscall":
            assembly = "syscall"

        # FORMATO TIPO R
        elif tipo == "r":
            if binario == "0" * 32:
                assembly = "nop"
            elif nome in ["sll", "srl", "sra"]:
                assembly = f"{nome} ${rd}, ${rt}, {shamt}"
            elif nome in ["sllv", "srlv", "srav"]:
                assembly = f"{nome} ${rd}, ${rt}, ${rs}"
            elif nome == "jr":
                assembly = f"{nome} ${rs}"
            elif nome in ["mfhi", "mflo"]:
                assembly = f"{nome} ${rd}"
            elif nome in ["mult", "multu", "div", "divu"]:
                assembly = f"{nome} ${rs}, ${rt}"
            else:
                assembly = f"{nome} ${rd}, ${rs}, ${rt}"

        # FORMATO TIPO I
        elif tipo == "i":
            immediate = int(immediate_bin, 2)
            # Extensão de sinal (sign-extension) para decimais negativos
            if nome not in ["andi", "ori", "xori"] and immediate >= 32768:
                immediate -= 65536

            if nome in ["lw", "sw", "lb", "lbu", "sb"]:
                assembly = f"{nome} ${rt}, {immediate}(${rs})"
            elif nome == "lui":
                assembly = f"{nome} ${rt}, {immediate}"
            elif nome in ["beq", "bne"]:
                assembly = f"{nome} ${rs}, ${rt}, {immediate}"
            elif nome in ["bgtz", "bltz", "blez"]:
                assembly = f"{nome} ${rs}, {immediate}"
            else:
                assembly = f"{nome} ${rt}, ${rs}, {immediate}"

        # FORMATO TIPO J
        elif tipo == "j":
            address = int(address_bin, 2)
            assembly = f"{nome} {address}"

        desassembled.append(assembly)

    return desassembled
