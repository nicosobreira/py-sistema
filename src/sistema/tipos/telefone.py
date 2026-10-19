import re

import sistema.erros as erros

DDI = "55"


class Telefone:
    ddd: str
    numero_quatro_primeiros: str
    numero_quatro_ultimos: str

    def __init__(self, telefone: str):
        if not self.verificar(telefone):
            raise erros.CadastroError

        formatado = self.normalizar(telefone)

        self.ddd = formatado[0:2]
        self.numero_quatro_primeiros = formatado[2:6]
        self.numero_quatro_ultimos = formatado[6:]

    def __str__(self) -> str:
        return f"({self.ddd}) {self.numero_quatro_primeiros}-{self.numero_quatro_ultimos}"

    @staticmethod
    def normalizar(telefone: str) -> str:
        return telefone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

    @staticmethod
    def verificar(telefone: str) -> bool:
        verificar = re.search(r"(^\(\d{2}\) \d{4}-\d{4}$)|(^\d{10}$)", telefone)

        return bool(verificar)
