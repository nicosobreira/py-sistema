import unicodedata
from dataclasses import dataclass

import leia

# TODO: Adicionar um formulario com setinhas, mais parecido com um TUI.


def remover_acentos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)

    return normalizado.encode("ascii", "ignore").decode("utf-8")


@dataclass
class InfoPessoal:
    nome: str
    cpf: str
    email: str
    telefone: str


@dataclass
class Aluno:
    info_pessoal: InfoPessoal
    prontuario: int
    codigo_curso: int


class Alunos:
    lista: list[Aluno]
    prontuario_count: int = 0

    def __init__(self):
        self.lista = []

    def _gerar_prontuario(self):
        gerado = self.prontuario_count

        self.prontuario_count += 1

        return gerado

    def adicionar(self, info_pessoal: InfoPessoal, codigo_curso: int):
        aluno = Aluno(
            info_pessoal=info_pessoal,
            prontuario=self._gerar_prontuario(),
            codigo_curso=codigo_curso,
        )

        self.lista.append(aluno)


class CursoTag:
    tag: str

    def __init__(self, nome: str):
        self.tag = self.formatar(nome)

    def formatar(self, nome: str) -> str:
        return remover_acentos(nome.lower().replace(" ", "_"))


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

        self.tags[curso.identificador.tag] = curso.codigo

        self.lista.append(curso)

    def _gerar_codigo(self) -> int:
        codigo = self.codigo_count

        self.codigo_count += 1

        return codigo

    def verificar_tag(self, nome: CursoTag) -> bool:
        return bool(self.tags.get(nome))

    def pegar_codigo(self, nome: CursoTag) -> int:
        return self.tags[nome]


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


TAB_TAMANHO = 8


def linha(simbolo: str, tamanho: int):
    print(f"{simbolo * tamanho}")


def titulo(texto: str):
    tamanho = TAB_TAMANHO * 2 + len(texto)
    tab = " " * TAB_TAMANHO

    linha("=", tamanho)
    print(f"{tab}{texto}")
    linha("=", tamanho)


def subtitulo(texto: str):
    tamanho = TAB_TAMANHO * 2 + len(texto)
    tab = " " * TAB_TAMANHO

    print(tab, end="")
    linha("=", tamanho)
    print(f"{tab}{tab}{texto}")
    print(tab, end="")
    linha("=", tamanho)


# Se o curso não existir, perguntar se não deseja criar um com o mesmo nome.
def curso_perguntar_codigo(cursos: Cursos) -> int:
    identificador = CursoIdentificador(leia.string("Digite o nome do curso"))

    if not cursos.verificar_tag(identificador.tag):
        subtitulo(f'Criando o novo curso "{identificador.nome}"')
        curso_criar(cursos, identificador)

    return cursos.pegar_codigo(identificador.tag)


def aluno_incluir(alunos: Alunos, cursos: Cursos):
    nome = leia.string("Digite o nome")
    cpf = leia.cpf()
    telefone = leia.telefone()
    email = leia.email()

    codigo_curso = curso_perguntar_codigo(cursos)

    info_pessoal = InfoPessoal(nome=nome, cpf=cpf, telefone=telefone, email=email)

    alunos.adicionar(info_pessoal, codigo_curso)


def aluno_alterar(alunos: Alunos):
    pass


def aluno_buscar(alunos: Alunos):
    pass


def aluno_excluir(alunos: Alunos):
    pass


def menu_aluno(alunos: Alunos, cursos: Cursos):
    aluno_opcoes = {"incluir": 1, "excluir": 2, "alterar": 3, "buscar": 4}

    while True:
        titulo("Aluno")

        opcao = leia.opcao_entre(aluno_opcoes)

        if opcao == aluno_opcoes["incluir"]:
            aluno_incluir(alunos, cursos)
        elif opcao == aluno_opcoes["alterar"]:
            aluno_alterar(alunos)
        elif opcao == aluno_opcoes["buscar"]:
            aluno_buscar(alunos)
        elif opcao == aluno_opcoes["excluir"]:
            aluno_excluir(alunos)
        else:
            break


def curso_criar(cursos: Cursos, identificador: CursoIdentificador | None):
    if identificador is None:
        identificador = CursoIdentificador(leia.string("Digite o nome do curso"))

    semestres = leia.inteiro_positivo("Quantidade de semestres")

    cursos.adicionar(identificador, semestres)


def curso_mostrar_alunos(cursos):
    pass


def menu_curso(cursos: Cursos):
    curso_opcoes = {
        "alunos": 1,
    }

    while True:
        titulo("Curso")

        opcao = leia.opcao_entre(curso_opcoes)

        if opcao == curso_opcoes["alunos"]:
            curso_mostrar_alunos(cursos)
        else:
            break


def disciplina_buscar_curso(disciplinas: Disciplinas):
    pass


def disciplina_buscar_semestre(disciplinas: Disciplinas):
    pass


def menu_disciplina(disciplinas: Disciplinas):
    disciplina_opcoes = {"buscar_semestre": 1, "buscar_curso": 2}

    while True:
        titulo("Disciplina")

        opcao = leia.opcao_entre(disciplina_opcoes)

        if opcao == disciplina_opcoes["buscar_curso"]:
            disciplina_buscar_curso(disciplinas)
        elif opcao == disciplina_opcoes["buscar_semestre"]:
            disciplina_buscar_semestre(disciplinas)
        else:
            break


def menu_principal(alunos: Alunos, cursos: Cursos, disciplinas: Disciplinas):
    area_opcoes: dict[str, int] = {"aluno": 1, "curso": 2, "disciplina": 3}

    while True:
        titulo("Menu Principal")

        opcao = leia.opcao_entre(area_opcoes)

        if opcao == area_opcoes["aluno"]:
            menu_aluno(alunos, cursos)
        elif opcao == area_opcoes["curso"]:
            menu_curso(cursos)
        elif opcao == area_opcoes["disciplina"]:
            menu_disciplina(disciplinas)
        else:
            break


def main():
    alunos = Alunos()
    cursos = Cursos()
    disciplinas = Disciplinas()

    menu_principal(alunos, cursos, disciplinas)


if __name__ == "__main__":
    main()
