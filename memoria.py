class Memoria:

    def __init__(self, dados=None):
        # Memória byte a byte
        self.mem = {}

        if dados:
            self.carregar(dados)

    def carregar(self, dados):
        for endereco, valor in dados.items():
            endereco = int(endereco)
            valor = int(valor) & 0xFF

            self.mem[endereco] = valor

    def ler_byte(self, endereco):
        return self.mem.get(endereco, 0)

    def escrever_byte(self, endereco, valor):
        valor = valor & 0xFF
        self.mem[endereco] = valor

    def ler_word(self, endereco):
        b0 = self.ler_byte(endereco)
        b1 = self.ler_byte(endereco + 1)
        b2 = self.ler_byte(endereco + 2)
        b3 = self.ler_byte(endereco + 3)

        valor = (
            (b0 << 24) |
            (b1 << 16) |
            (b2 << 8) |
            b3
        )

        if valor & 0x80000000:
            valor -= 0x100000000

        return valor

    def escrever_word(self, endereco, valor):
        valor = valor & 0xFFFFFFFF

        b0 = (valor >> 24) & 0xFF
        b1 = (valor >> 16) & 0xFF
        b2 = (valor >> 8) & 0xFF
        b3 = valor & 0xFF

        self.escrever_byte(endereco, b0)
        self.escrever_byte(endereco + 1, b1)
        self.escrever_byte(endereco + 2, b2)
        self.escrever_byte(endereco + 3, b3)

    def exportar_para_json(self):
        resultado = {}

        for endereco, valor in sorted(self.mem.items()):
            if valor != 0:
                resultado[str(endereco)] = valor

        return resultado