import unicodedata


def remover_acentos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)

    return normalizado.encode("ascii", "ignore").decode("utf-8")


def normalizado(texto: str) -> str:
    return remover_acentos(texto.lower()).replace(" ", "_")


def normalizar_telefone(telefone: str) -> str:
    return telefone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
