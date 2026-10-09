import re

OPCAO_SAIR = 0


def string(mensagem: str) -> str:
    print(f"{mensagem}.")
    return input("> ")


def inteiro_entre(mensagem: str, validos: list[int]) -> int:
    minimo = OPCAO_SAIR
    maximo = max(validos)

    print(mensagem)
    while True:
        try:
            resposta = int(input("> "))
        except ValueError:
            print("Digite um número!")
            continue

        if minimo <= resposta <= maximo:
            return resposta
        else:
            print(f"Opção inválida! Escolha entre: {minimo} e {maximo}.")


def inteiro_positivo(mensagem: str) -> int:
    print(mensagem)

    while True:
        try:
            resposta = int(input("> "))
        except ValueError:
            print("Digite um número!")
            continue

        if resposta > 0:
            return resposta
        else:
            print("Digite um número maior do que 0")


"""
def _validar_telefone(tel: str) -> bool:
    verificar = re.search("^\\(\\d{2}\\) \\d{4}-\\d{4}$", tel)

    return bool(verificar)
"""


def telefone() -> str:
    # TODO: Verificar o tamanho do telefone
    while True:
        tel = string("Digite o telefone")

        return tel


"""
def _validar_cpf(cpf: str) -> bool:
    verificar = re.search("^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$", cpf)

    return bool(verificar)
"""


def cpf() -> str:
    # TODO:Verificar o tamanho do CPF
    while True:
        cpf = string("Digite o CPF")

        return cpf


def _validar_email(email: str) -> bool:
    verificar = re.search(r"^[\w.-]+@([\w-]+\.)+[\w-]{2,}$", email)

    return bool(verificar)


def email() -> str:
    while True:
        email = string("Digite o Email")

        if _validar_email(email):
            return email
        else:
            print("Formato errado! Digite novamente")


def opcao_entre(opcoes: dict[str, int]) -> int:
    validos = []

    for opcao, id in opcoes.items():
        print(f"{id} - {opcao.capitalize()}")
        validos.append(id)

    return inteiro_entre(f"Digite uma das opções acima ({OPCAO_SAIR} para sair)", validos)


def confirmar(mensagem: str) -> bool:
    formato = "[S/N]"
    print(f"{mensagem} {formato}.")

    while True:
        opcao = input("> ").lower()

        if opcao in ("s", "sim"):
            return True
        elif opcao in ("n", "nao", "não"):
            return False
        else:
            print("Erro, digite novamente")
