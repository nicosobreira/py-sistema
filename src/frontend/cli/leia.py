import re

import sistema.erros
from sistema.tipos.cpf import Cpf
from sistema.tipos.email import Email
from sistema.tipos.telefone import Telefone

from . import erros, mostre

OPCAO_VOLTAR = 0


def leia():
    try:
        entrada = input("> ")
    except KeyboardInterrupt:
        exit()

    return entrada


def string(mensagem: str) -> str:
    mostre.mensagem(f"{mensagem}")
    return leia()


def inteiro_entre(mensagem: str, maximo: int) -> int:
    minimo = OPCAO_VOLTAR

    mostre.mensagem(mensagem + f" ({OPCAO_VOLTAR} para voltar)")
    while True:
        try:
            resposta = int(leia())
        except ValueError:
            mostre.erro("Digite um número!")
            continue

        if minimo <= resposta <= maximo:
            return resposta
        else:
            mostre.erro(f"Opção inválida! Escolha entre: {minimo} e {maximo}.")


def varios_inteiros_entre(mensagem: str, maximo: int) -> list[int]:
    minimo = OPCAO_VOLTAR
    respostas = []

    mostre.mensagem(mensagem)

    while True:
        try:
            respostas = list(map(int, leia().split(" ")))
        except ValueError:
            mostre.erro("Digite um número!")
            continue

        for resposta in respostas:
            if resposta > maximo:
                mostre.erro(f'Opção "{resposta}" inválida! Escolha entre: {minimo} e {maximo}.')
                break
        else:
            break

    return respostas


def inteiro_positivo(mensagem: str) -> int:
    return inteiro_maior_igual(mensagem, 1)


def inteiro_maior_igual(mensagem: str, maior_igual: int) -> int:
    mostre.mensagem(mensagem)

    while True:
        try:
            resposta = int(leia())
        except ValueError:
            mostre.erro("Digite um número!")
            continue

        if resposta >= maior_igual:
            return resposta
        else:
            mostre.erro(f"Digite um número maior do que {maior_igual}!")


def telefone() -> Telefone:
    # TODO: Verificar o tamanho do telefone
    while True:
        try:
            telefone = Telefone(string("Digite o telefone."))
        except sistema.erros.CadastroError:
            mostre.erro("Digite um telefone válido!")
        else:
            return telefone


def cpf() -> Cpf:
    # TODO:Verificar o tamanho do CPF
    while True:
        try:
            cpf = Cpf(string("Digite o CPF."))
        except sistema.erros.CadastroError:
            mostre.erro("Digite um cpf válido!")
        else:
            return cpf


def email() -> Email:
    while True:
        try:
            email = Email(string("Digite o Email."))
        except sistema.erros.CadastroError:
            mostre.erro("Digite um email válido!")
        else:
            return email


def uma_opcao_entre(opcoes: dict[str, int]) -> int:
    maximo = len(opcoes)

    mostre.mostrar_opcoes(opcoes)

    return inteiro_entre("Digite uma das opções acima.", maximo)


def varias_opcoes_entre(opcoes: dict[str, int]) -> list[int]:
    maximo = len(opcoes)

    mostre.mostrar_opcoes(opcoes)

    return varios_inteiros_entre(
        f"Digite as opções que deseja escolher separadas por um espaço ({OPCAO_VOLTAR} para sair)",
        maximo,
    )


def confirmar(mensagem: str) -> bool:
    formato = "[S/N]"
    mostre.mensagem(f"{mensagem} {formato}")

    while True:
        opcao = leia().lower()

        if opcao in ("s", "sim"):
            return True
        elif opcao in ("n", "nao", "não"):
            return False
        else:
            mostre.erro("Erro, digite novamente!")
