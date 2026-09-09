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
            if opcode == instrucao[1]["opcode"] and funct == instrucao[1]["funct"]:
                if instrucao[1]["tipo"] == 'r':
                    opcode = binario[:6]
                    rs = binario[6:11]
                    rt = binario[11:16]
                    rd = binario[16:21]
                    shamt = binario[21:26]
                    funct = binario[26:]
                    desassembled.append((opcode, rs, rt, rd, shamt, funct))
                elif instrucao[1]["tipo"] == 'i':
                    opcode = binario[:6]
                    rs = binario[6:11]
                    rt = binario[11:16]
                    immediate = binario[16:]
                    desassembled.append((opcode, rs, rt, immediate))
                elif instrucao[1]["tipo"] == 'j':
                    opcode = binario[:6]
                    address = binario[6:]
                    desassembled.append((opcode, address))
                elif instrucao[1]["tipo"] is None:
                    desassembled.append((opcode, funct))
            if opcode == instrucao[1]["opcode"] and funct == instrucao[1]["funct"]:
                if instrucao[1]["tipo"] == 'r':
                    opcode = binario[:6]
                    rs = binario[6:11]
                    rt = binario[11:16]
                    rd = binario[16:21]
                    shamt = binario[21:26]
                    funct = binario[26:]
                    desassembled.append((opcode, rs, rt, rd, shamt, funct))
                elif instrucao[1]["tipo"] == 'i':
                    opcode = binario[:6]
                    rs = binario[6:11]
                    rt = binario[11:16]
                    immediate = binario[16:]
                    desassembled.append((opcode, rs, rt, immediate))
                elif instrucao[1]["tipo"] == 'j':
                    opcode = binario[:6]
                    address = binario[6:]
                    desassembled.append((opcode, address))
                elif instrucao[1]["tipo"] is None:
                    desassembled.append((opcode, funct))
                else:
                    desassembled.append(("Instrução desconhecida", binario))

    return desassembled