# INSTRUÇÕES MIPS

instrucoesMips = {
    "add": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100000'
    },
    "addi": {
        "tipo": 'i',
        "opcode": '001000',
        "funct": None
    },
    "addiu": {
        "tipo": 'i',
        "opcode": '001001',
        "funct": None
    },
    "addu": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100001'
    },
    "and": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100100'
    },
    "andi": {
        "tipo": 'i',
        "opcode": '001100',
        "funct": None
    },
    "bgtz": {
        "tipo": 'i',
        "opcode": '000111',
        "funct": None
    },
    "beq": {
        "tipo": 'i',
        "opcode": '000100',
        "funct": None
    },
    "bltz": {
        "tipo": 'i',
        "opcode": '000001',
        "funct": None
    },
    "blez": {
        "tipo": 'i',
        "opcode": '000110',
        "funct": None
    },
    "bne": {
        "tipo": 'i',
        "opcode": '000101',
        "funct": None
    },
    "div": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '011010'
    },
    "divu": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '011011'
    },
    "j": {
        "tipo": 'j',
        "opcode": '000010',
        "funct": None
    },
    "jal": {
        "tipo": 'j',
        "opcode": '000011',
        "funct": None
    },
    "jr": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '001000'
    },
    "lb": {
        "tipo": 'i',
        "opcode": '100000',
        "funct": None
    },
    "lbu": {
        "tipo": 'i',
        "opcode": '100100',
        "funct": None
    },
    "lui": {
        "tipo": 'i',
        "opcode": '001111',
        "funct": None
    },
    "lw": {
        "tipo": 'i',
        "opcode": '100011',
        "funct": None
    },
    "mfhi": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '010000'
    },
    "mflo": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '010010'
    },
    "mult": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '011000'
    },
    "multu": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '011001'
    },
    "nor": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100111'
    },
    "or": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100101'
    },
    "ori": {
        "tipo": 'i',
        "opcode": '001101',
        "funct": None
    },
    "sb": {
        "tipo": 'i',
        "opcode": '101000',
        "funct": None
    },
    "sll": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '000000'
    },
    "sllv": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '000100'
    },
    "slt": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '101010'
    },
    "slti": {
        "tipo": 'i',
        "opcode": '001010',
        "funct": None
    },
    "sra": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '000011'
    },
    "srav": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '000111'
    },
    "srl": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '000010'
    },
    "srlv": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '000110'
    },
    "sub": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100010'
    },
    "subu": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100011'
    },
    "sw": {
        "tipo": 'i',
        "opcode": '101011',
        "funct": None
    },
    "syscall": {
        "tipo": None,
        "opcode": '000000',
        "funct": '001100'
    },
    "xor": {
        "tipo": 'r',
        "opcode": '000000',
        "funct": '100110'
    },
    "xori": {
        "tipo": 'i',
        "opcode": '001110',
        "funct": None
    },
}

def get_instrucao_mips(instrucoesBinarias):
    
    desassembled = []
    
    for binario in instrucoesBinarias:
        opcode = binario[:6]
        funct = binario[26:]

        for instrucao in instrucoesMips.items():
            opcode = binario[:6]
        rs = int(binario[6:11], 2)
        rt = int(binario[11:16], 2)
        rd = int(binario[16:21], 2)
        shamt = int(binario[21:26], 2)
        funct = binario[26:]

        immediate_bin = binario[16:]
        address_bin = binario[6:]

        instrucao_encontrada = None

        # IDENTIFICA A INSTRUÇÃO
        for nome, dados in instrucoesMips.items():

            # Tipo R
            if dados["tipo"] == "r":
                if opcode == dados["opcode"] and funct == dados["funct"]:
                    instrucao_encontrada = nome
                    break

            # Tipo I
            elif dados["tipo"] == "i":
                if opcode == dados["opcode"]:
                    instrucao_encontrada = nome
                    break

            # Tipo J
            elif dados["tipo"] == "j":
                if opcode == dados["opcode"]:
                    instrucao_encontrada = nome
                    break

            # syscall
            elif dados["tipo"] is None:
                if opcode == dados["opcode"] and funct == dados["funct"]:
                    instrucao_encontrada = nome
                    break

        # Se não encontrou
        if instrucao_encontrada is None:
            desassembled.append(f"Instrução desconhecida: {binario}")
            continue

        nome = instrucao_encontrada
        tipo = instrucoesMips[nome]["tipo"]

        # TIPO R

        if tipo == "r":

            if nome in ["sll", "srl", "sra"]:
                assembly = f"{nome} ${rd}, ${rt}, {shamt}"

            elif nome in ["sllv", "srlv", "srav"]:
                assembly = f"{nome} ${rd}, ${rt}, ${rs}"

            elif nome == "jr":
                assembly = f"{nome} ${rs}"

            elif nome in ["mfhi", "mflo"]:
                assembly = f"{nome} ${rd}"

            elif nome in ["mult", "multu", "div", "divu"]:
                assembly = f"{nome} ${rs}, ${rt}"

            elif nome == "syscall":
                assembly = "syscall"

            else:
                assembly = f"{nome} ${rd}, ${rs}, ${rt}"

        # TIPO I

        elif tipo == "i":

            immediate = int(immediate_bin, 2)

            # Converte para signed 16 bits

            if immediate >= 32768:
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

        # TIPO J

        elif tipo == "j":

            address = int(address_bin, 2)

            assembly = f"{nome} {address}"

        desassembled.append(assembly)

    return desassembled