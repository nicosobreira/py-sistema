from dataclasses import dataclass

import utils


class CursoTag:
    tag: str

    def __init__(self, nome: str):
        self.tag = self.formatar(nome)

    def formatar(self, nome: str) -> str:
        return utils.normalizado(nome)

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


class Cursos:
    lista: list[Curso]
    tags: dict[CursoTag, int]
    codigo_count: int = 0

    def __init__(self):
        self.lista = []
        self.tags = {}
        self.codigo_count = 0

    def adicionar(self, identificador: CursoIdentificador, semestres: int):
        curso = Curso(identificador=identificador, semestres=semestres, codigo=self._gerar_codigo())

        self.tags.setdefault(curso.identificador.tag, curso.codigo)

        self.lista.append(curso)

    def _gerar_codigo(self) -> int:
        codigo = self.codigo_count

        self.codigo_count += 1

        return codigo

    def verificar_tag(self, nome: CursoTag) -> bool:
        return bool(self.tags.get(nome))

    def pegar_codigo(self, nome: CursoTag) -> int | None:
        return self.tags.get(nome)

    # CursoInexistenteError
    def pegar_identificador(self, codigo: int) -> CursoIdentificador | None:
        for curso in self.lista:
            if curso.codigo == codigo:
                return curso.identificador

        return None

    def pegar_tag(self, codigo: int) -> CursoTag | None:
        identi = self.pegar_identificador(codigo)

        if identi is None:
            return None

        return identi.tag

    def esta_vazio(self) -> bool:
        return len(self.lista) == 0
