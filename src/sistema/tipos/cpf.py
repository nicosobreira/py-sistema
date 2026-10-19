import re

import sistema.erros as erros


class Cpf:
    # Grupos de 3 números separados por pontos
    g1: str
    g2: str
    g3: str

    # Dupla de números final separado por "-"
    dupla: str

    def __init__(self, cpf: str):
        if not self.verificar(cpf):
            raise erros.CadastroError

        cpf = self.normalizar(cpf)

        self.g1 = cpf[0:3]
        self.g2 = cpf[3:6]
        self.g3 = cpf[6:9]
        self.dupla = cpf[9:]

    def __str__(self) -> str:
        return f"{self.g1}.{self.g2}.{self.g3}-{self.dupla}"

    @staticmethod
    def normalizar(cpf: str) -> str:
        return cpf.replace(".", "").replace("-", "")

    @staticmethod
    def verificar(cpf: str) -> bool:
        verificar = re.search(r"(^\d{3}\.\d{3}\.\d{3}-\d{2}$)|(^\d{11}$)", cpf)

        return bool(verificar)
