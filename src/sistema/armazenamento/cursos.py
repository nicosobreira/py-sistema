from sistema.tipos.curso import Curso, CursoIdentificador, CursoTag


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

    def pegar_identificador(self, codigo: int) -> CursoIdentificador | None:
        for curso in self.lista:
            if curso.codigo == codigo:
                return curso.identificador

        return None

    def esta_vazio(self) -> bool:
        return len(self.lista) == 0
