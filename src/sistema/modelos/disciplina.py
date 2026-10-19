from dataclasses import dataclass


@dataclass
class Disciplina:
    id: int
    nome: str
    codigo_curso: int
    semestre: int


class Disciplinas:
    lista: list[Disciplina]

    def __init__(self):
        self.lista = []
