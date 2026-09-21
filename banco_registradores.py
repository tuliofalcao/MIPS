"""
Módulo responsável pelo gerenciamento do Banco de Registradores do MIPS.
Atende às especificações da Entrega 2 do projeto.
"""

class BancoRegistradores:
    # Endereços iniciais padrão do simulador MARS em Hexadecimal
    VALOR_INICIAL_GP = 0x10008000  # $28
    VALOR_INICIAL_SP = 0x7FFFEFFC  # $29
    VALOR_INICIAL_PC = 0x00400000  # Program Counter

    def __init__(self, config: dict = None):
        """
        Inicializa os 32 registradores gerais (32 bits cada) e os registradores
        especiais PC, HI e LO com os padrões do MARS e aplica as configurações customizadas.
        """
        # Inicializa todos os 32 registradores gerais com valor 0
        self.regs = {i: 0 for i in range(32)}
        
        # Define os valores padrão do MARS
        self.regs[28] = self.VALOR_INICIAL_GP  # $gp ($28)
        self.regs[29] = self.VALOR_INICIAL_SP  # $sp ($29)
        self.pc = self.VALOR_INICIAL_PC        # Program Counter
        self.hi = 0                            # Registrador HI (32 bits mais significativos)
        self.lo = 0                            # Registrador LO (32 bits menos significativos)

        # Se houver configurações iniciais na entrada JSON, aplica-as
        if config:
            self._aplicar_configuracao_inicial(config)

    def _aplicar_configuracao_inicial(self, config: dict) -> None:
        """
        Carrega valores do campo 'config' do entrada.json no banco de registradores.
        """
        for chave, valor in config.items():
            chave_limpa = str(chave).strip().lower()
            
            # Atualização dos registradores especiais
            if chave_limpa == "pc":
                self.pc = self._ajustar_32bits(valor)
            elif chave_limpa == "hi":
                self.hi = self._ajustar_32bits(valor)
            elif chave_limpa == "lo":
                self.lo = self._ajustar_32bits(valor)
            else:
                # Tratamento para "$8", "8" ou "r8"
                num_str = chave_limpa.replace("$", "").replace("r", "")
                if num_str.isdigit():
                    num_reg = int(num_str)
                    if 0 < num_reg < 32:  # O registrador $0 nunca é alterado
                        self.regs[num_reg] = self._ajustar_32bits(valor)

    def _ajustar_32bits(self, valor: int) -> int:
        """
        Garante que o valor armazenado esteja restrito ao limite de 32 bits com sinal.
        """
        valor_32 = valor & 0xFFFFFFFF
        if valor_32 & 0x80000000:  # Se o bit de sinal estiver ativo
            valor_32 -= 0x100000000
        return valor_32

    def ler(self, reg_num: int) -> int:
        """
        Retorna o valor contido no registrador especificado.
        O registrador $0 sempre retornará 0.
        """
        if reg_num == 0:
            return 0
        return self.regs.get(reg_num, 0)

    def escrever(self, reg_num: int, valor: int) -> None:
        """
        Escreve um valor de 32 bits no registrador especificado.
        Tentativas de escrita no registrador $0 são ignoradas.
        """
        if reg_num == 0:
            return  # $0 é imutável
        self.regs[reg_num] = self._ajustar_32bits(valor)

    def exportar_para_json(self) -> dict:
        """
        Retorna um dicionário contendo APENAS os registradores cujos valores
        sejam diferentes de zero, conforme exigido nas regras da Entrega 2.
        """
        resultado = {}

        # 1. Registradores gerais ($1 até $31)
        for num in range(32):
            if self.regs[num] != 0:
                resultado[f"${num}"] = self.regs[num]

        # 2. Registradores especiais (PC, HI, LO)
        if self.pc != 0:
            resultado["pc"] = self.pc
        if self.hi != 0:
            resultado["hi"] = self.hi
        if self.lo != 0:
            resultado["lo"] = self.lo

        return resultado
