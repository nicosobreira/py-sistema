from dataclasses import dataclass

import sistema.formatacao as format


class CursoTag:
    tag: str

    def __init__(self, nome: str):
        self.tag = self.formatar(nome)

    def formatar(self, nome: str) -> str:
        return format.normalizar(nome)

    def __hash__(self) -> int:
        return hash(self.tag)

    def __eq__(self, outro):
        return isinstance(outro, CursoTag) and self.tag == outro.tag


# TODO: Será que eu coloco o código do curso como um identificador?
# Ai eu poderia ter um dicionário com o `CursoTag` e os outros atributos, como
# o usuário vai digitar o nome do curso ou o codigo dele
# TODO: O usuário vai acessar o curso a partir do NOME ou CÓDIGO, como fazer a busca pelo
# curso se aproveitar disso?
@dataclass
class CursoIdentificador:
    tag: CursoTag
    nome: str

    def __init__(self, nome):
        self.nome = nome
        self.tag = CursoTag(nome)


@dataclass
class Curso:
    identificador: CursoIdentificador
    codigo: int
    semestres: int
