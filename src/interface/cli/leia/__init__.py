import re

from .. import style

OPCAO_VOLTAR = 0


def string(mensagem: str) -> str:
    style.mensagem(f"{mensagem}.")
    return input("> ")


def inteiro_entre(mensagem: str, maximo: int) -> int:
    minimo = OPCAO_VOLTAR

    style.mensagem(mensagem + " (0 para voltar)")
    while True:
        try:
            resposta = int(input("> "))
        except ValueError:
            style.erro("Digite um número!")
            continue

        if minimo <= resposta <= maximo:
            return resposta
        else:
            style.erro(f"Opção inválida! Escolha entre: {minimo} e {maximo}.")


def varios_inteiros_entre(mensagem: str, maximo: int) -> list[int] | None:
    minimo = OPCAO_VOLTAR
    respostas = []

    style.mensagem(mensagem)

    while True:
        try:
            respostas = list(map(int, input("> ").split(" ")))
        except ValueError:
            style.erro("Digite um número!")
            continue

        for resposta in respostas:
            if resposta > maximo:
                style.erro(f'Opção "{resposta}" inválida! Escolha entre: {minimo} e {maximo}.')
                break
        else:
            break

    return respostas


def inteiro_positivo(mensagem: str) -> int:
    return inteiro_maior_igual(mensagem, 1)


def inteiro_maior_igual(mensagem: str, maior_igual: int) -> int:
    style.mensagem(mensagem)

    while True:
        try:
            resposta = int(input("> "))
        except ValueError:
            style.erro("Digite um número!")
            continue

        if resposta >= maior_igual:
            return resposta
        else:
            style.erro(f"Digite um número maior do que {maior_igual}")


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
            style.erro("Formato errado! Digite novamente")


def uma_opcao_entre(opcoes: dict[str, int]) -> int:
    maximo = len(opcoes)

    style.mostrar_opcoes(opcoes)

    return inteiro_entre("Digite uma das opções acima", maximo)


def varias_opcoes_entre(opcoes: dict[str, int]) -> list[int] | None:
    maximo = len(opcoes)

    style.mostrar_opcoes(opcoes)

    return varios_inteiros_entre(
        "Digite as opções que deseja escolher separadas por um espaço", maximo
    )


def confirmar(mensagem: str) -> bool:
    formato = "[S/N]"
    style.mensagem(f"{mensagem}? {formato}")

    while True:
        opcao = input("> ").lower()

        if opcao in ("s", "sim"):
            return True
        elif opcao in ("n", "nao", "não"):
            return False
        else:
            style.erro("Erro, digite novamente")
