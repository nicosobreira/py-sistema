from dataclasses import dataclass


@dataclass
class Disciplina:
    id: int
    nome: str
    codigo_curso: int
    semestre: int
