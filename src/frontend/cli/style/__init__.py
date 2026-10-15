from . import ansi

TAB_TAMANHO = 8

TAB = " " * TAB_TAMANHO
TAB_METADE = " " * int(TAB_TAMANHO / 2)


def mensagem(mensagem: str):
    print(mensagem)


def separador():
    print()


def aviso(mensagem: str):
    print(ansi.AMARELO + "AVISO: " + ansi.RESET + mensagem)


def erro(mensagem: str):
    print(ansi.VERMELHO + "ERRO: " + ansi.RESET + mensagem)


def lista(mensagens: list[str]):
    tab = TAB_METADE
    for mensagem in mensagens:
        print(f"{tab}{mensagem}")


def sucesso(mensagem: str):
    print(ansi.VERDE + "SUCESSO: " + ansi.RESET + mensagem)


def format_chave(chave: str) -> str:
    return chave.replace("_", " ").title()


def linha(simbolo: str, tamanho: int):
    print(f"{simbolo * tamanho}")


def titulo_1(texto: str):
    tamanho = TAB_TAMANHO * 2 + len(texto)

    separador()
    linha("=", tamanho)
    print(f"{TAB}{texto}")
    linha("=", tamanho)


def titulo_2(texto: str):
    tamanho = TAB_TAMANHO * 2 + len(texto)

    print(TAB, end="")
    linha("=", tamanho)
    print(f"{TAB}{TAB}{texto}")
    print(TAB, end="")
    linha("=", tamanho)


def titulo_3(texto: str):
    print(f"  --- {texto} ---")


def mostrar_opcoes(opcoes: dict[str, int]):
    tab = TAB_METADE

    for opcao, id in opcoes.items():
        print(f"{tab}{id} - {format_chave(opcao)}")
