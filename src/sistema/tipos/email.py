import re

import sistema.erros as erros


class Email:
    def __init__(self, email: str):
        if not self.verificar(email):
            raise erros.CadastroError

        self.email = email

    def __str__(self):
        return self.email

    @staticmethod
    def verificar(email: str) -> bool:
        verificar = re.search(r"^[\w.-]+@([\w-]+\.)+[\w-]{2,}$", email)

        return bool(verificar)
