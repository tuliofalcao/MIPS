from banco_registradores import BancoRegistradores
from memoria import Memoria


def ajustar_32bits(valor):
    """
    Mantém o valor dentro de 32 bits com sinal.
    """
    valor = valor & 0xFFFFFFFF

    if valor & 0x80000000:
        valor -= 0x100000000

    return valor


def executar_instrucao(binario, banco, memoria):
    """
    Executa uma instrução MIPS e atualiza o banco de registradores.
    """

    opcode = binario[:6]

    rs = int(binario[6:11], 2)
    rt = int(binario[11:16], 2)
    rd = int(binario[16:21], 2)
    shamt = int(binario[21:26], 2)
    funct = binario[26:]

    imediato = int(binario[16:], 2)

    # Converte imediato de 16 bits para signed
    imediato_signed = imediato

    if imediato >= 32768:
        imediato_signed -= 65536

    # Valores dos registradores
    valor_rs = banco.ler(rs)
    valor_rt = banco.ler(rt)

    # =========================================================
    # INSTRUÇÕES TIPO R
    # =========================================================

    if opcode == "000000":

        # ADD
        if funct == "100000":
            resultado = valor_rs + valor_rt
            banco.escrever(rd, ajustar_32bits(resultado))

        # ADDU
        elif funct == "100001":
            resultado = valor_rs + valor_rt
            banco.escrever(rd, ajustar_32bits(resultado))

        # SUB
        elif funct == "100010":
            resultado = valor_rs - valor_rt
            banco.escrever(rd, ajustar_32bits(resultado))

        # SUBU
        elif funct == "100011":
            resultado = valor_rs - valor_rt
            banco.escrever(rd, ajustar_32bits(resultado))

        # AND
        elif funct == "100100":
            resultado = valor_rs & valor_rt
            banco.escrever(rd, ajustar_32bits(resultado))

        # OR
        elif funct == "100101":
            resultado = valor_rs | valor_rt
            banco.escrever(rd, ajustar_32bits(resultado))

        # XOR
        elif funct == "100110":
            resultado = valor_rs ^ valor_rt
            banco.escrever(rd, ajustar_32bits(resultado))

        # NOR
        elif funct == "100111":
            resultado = ~(valor_rs | valor_rt)
            banco.escrever(rd, ajustar_32bits(resultado))

        # SLT
        elif funct == "101010":
            if valor_rs < valor_rt:
                banco.escrever(rd, 1)
            else:
                banco.escrever(rd, 0)

        # SLL
        elif funct == "000000":
            resultado = valor_rt << shamt
            banco.escrever(rd, ajustar_32bits(resultado))

        # SRL
        elif funct == "000010":
            valor = valor_rt & 0xFFFFFFFF
            resultado = valor >> shamt
            banco.escrever(rd, ajustar_32bits(resultado))

        # SRA
        elif funct == "000011":
            resultado = valor_rt >> shamt
            banco.escrever(rd, ajustar_32bits(resultado))

        # SLLV
        elif funct == "000100":
            quantidade = valor_rs & 0x1F
            resultado = valor_rt << quantidade
            banco.escrever(rd, ajustar_32bits(resultado))

        # SRLV
        elif funct == "000110":
            quantidade = valor_rs & 0x1F
            valor = valor_rt & 0xFFFFFFFF
            resultado = valor >> quantidade
            banco.escrever(rd, ajustar_32bits(resultado))

        # SRAV
        elif funct == "000111":
            quantidade = valor_rs & 0x1F
            resultado = valor_rt >> quantidade
            banco.escrever(rd, ajustar_32bits(resultado))

        # MFHI
        elif funct == "010000":
            banco.escrever(rd, banco.hi)

        # MFLO
        elif funct == "010010":
            banco.escrever(rd, banco.lo)

        # MULT
        elif funct == "011000":

            resultado = valor_rs * valor_rt

            resultado = resultado & 0xFFFFFFFFFFFFFFFF

            banco.hi = (resultado >> 32) & 0xFFFFFFFF
            banco.lo = resultado & 0xFFFFFFFF

            banco.hi = ajustar_32bits(banco.hi)
            banco.lo = ajustar_32bits(banco.lo)

        # MULTU
        elif funct == "011001":

            rs_unsigned = valor_rs & 0xFFFFFFFF
            rt_unsigned = valor_rt & 0xFFFFFFFF

            resultado = rs_unsigned * rt_unsigned

            banco.hi = (resultado >> 32) & 0xFFFFFFFF
            banco.lo = resultado & 0xFFFFFFFF

            banco.hi = ajustar_32bits(banco.hi)
            banco.lo = ajustar_32bits(banco.lo)

        # DIV
        elif funct == "011010":

            if valor_rt != 0:

                quociente = int(valor_rs / valor_rt)
                resto = valor_rs - (quociente * valor_rt)

                banco.lo = ajustar_32bits(quociente)
                banco.hi = ajustar_32bits(resto)

        # DIVU
        elif funct == "011011":

            rs_unsigned = valor_rs & 0xFFFFFFFF
            rt_unsigned = valor_rt & 0xFFFFFFFF

            if rt_unsigned != 0:

                quociente = rs_unsigned // rt_unsigned
                resto = rs_unsigned % rt_unsigned

                banco.lo = ajustar_32bits(quociente)
                banco.hi = ajustar_32bits(resto)

    # =========================================================
    # INSTRUÇÕES TIPO I
    # =========================================================

    # ADDI
    elif opcode == "001000":

        resultado = valor_rs + imediato_signed

        banco.escrever(
            rt,
            ajustar_32bits(resultado)
        )

    # ADDIU
    elif opcode == "001001":

        resultado = valor_rs + imediato_signed

        banco.escrever(
            rt,
            ajustar_32bits(resultado)
        )

    # SLTI
    elif opcode == "001010":

        if valor_rs < imediato_signed:
            banco.escrever(rt, 1)
        else:
            banco.escrever(rt, 0)

    # ANDI
    elif opcode == "001100":

        resultado = (
            valor_rs &
            imediato
        )

        banco.escrever(
            rt,
            ajustar_32bits(resultado)
        )

    # ORI
    elif opcode == "001101":

        resultado = (
            valor_rs |
            imediato
        )

        banco.escrever(
            rt,
            ajustar_32bits(resultado)
        )

    # XORI
    elif opcode == "001110":

        resultado = (
            valor_rs ^
            imediato
        )

        banco.escrever(
            rt,
            ajustar_32bits(resultado)
        )

    # LUI

    elif opcode == "001111":

        resultado = imediato << 16

        banco.escrever(
            rt,
            ajustar_32bits(resultado)
        )


    # LOAD E STORE

    # LB
    elif opcode == "100000":

        endereco = valor_rs + imediato_signed

        valor = memoria.ler_byte(endereco)

        if valor >= 128:
            valor -= 256

        banco.escrever(rt, valor)

    # LBU
    elif opcode == "100100":

        endereco = valor_rs + imediato_signed

        valor = memoria.ler_byte(endereco)

        banco.escrever(rt, valor)

    # LW
    elif opcode == "100011":

        endereco = valor_rs + imediato_signed

        valor = memoria.ler_word(endereco)

        banco.escrever(rt, valor)

    # SB
    elif opcode == "101000":

        endereco = valor_rs + imediato_signed

        valor = valor_rt & 0xFF

        memoria.escrever_byte(
            endereco,
            valor
        )

    # SW
    elif opcode == "101011":

        endereco = valor_rs + imediato_signed

        memoria.escrever_word(
            endereco,
            valor_rt
        )

    # =========================================================
    # DESVIOS
    # =========================================================

    # BEQ
    elif opcode == "000100":

        if valor_rs == valor_rt:
            banco.pc += imediato_signed * 4

    # BNE
    elif opcode == "000101":

        if valor_rs != valor_rt:
            banco.pc += imediato_signed * 4

    # BGTZ
    elif opcode == "000111":

        if valor_rs > 0:
            banco.pc += imediato_signed * 4

    # BLTZ
    elif opcode == "000001":

        if valor_rs < 0:
            banco.pc += imediato_signed * 4

    # BLEZ
    elif opcode == "000110":

        if valor_rs <= 0:
            banco.pc += imediato_signed * 4

    # =========================================================
    # DESVIOS TIPO J
    # =========================================================

    # J
    elif opcode == "000010":

        endereco = int(binario[6:], 2)

        banco.pc = (banco.pc & 0xF0000000) | (endereco << 2)

    # JAL
    elif opcode == "000011":

        endereco = int(binario[6:], 2)

        banco.escrever(
            31,
            banco.pc + 4
        )

        banco.pc = (banco.pc & 0xF0000000) | (endereco << 2)