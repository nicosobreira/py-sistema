import unicodedata
from dataclasses import dataclass, fields

import frontend.cli.leia as leia
import frontend.cli.style as style

# TODO: Adicionar um formulario com setinhas, mais parecido com um TUI.


def remover_acentos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)

    return normalizado.encode("ascii", "ignore").decode("utf-8")


def normalizado(texto: str) -> str:
    return remover_acentos(texto.lower()).replace(" ", "_")


def normalizar_telefone(telefone: str) -> str:
    return telefone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")


@dataclass
class AlunoPublico:
    codigo_curso: int
    nome: str
    email: str
    telefone: str
    prontuario: int = -1


@dataclass
class AlunoPrivado:
    cpf: str


@dataclass
class Aluno:
    privado: AlunoPrivado
    publico: AlunoPublico


ALUNO_CAMPOS_PUBLICOS = {f.name for f in fields(AlunoPublico)}


class Alunos:
    lista: list[Aluno]
    prontuario_count: int

    def __init__(self):
        self.lista = []
        self.prontuario_count = 0
        self._comparadores = {
            "nome": self._procurar_nome,
            "email": self._procurar_email,
            "telefone": self._procurar_telefone,
            "codigo_curso": self._procurar_codigo_curso,
            "prontuario": self._procurar_prontuario,
        }

    def _gerar_prontuario(self):
        gerado = self.prontuario_count

        self.prontuario_count += 1

        return gerado

    # TODO: Adicionar exceptions se o email ou telefone forem iguais
    def adicionar(self, privado: AlunoPrivado, publico: AlunoPublico):
        aluno = Aluno(privado=privado, publico=publico)

        aluno.publico.prontuario = self._gerar_prontuario()

        self.lista.append(aluno)

    # Sem dados sensíveis
    def lista_publica(self) -> list[AlunoPublico]:
        compartilhar = []

        for aluno in self.lista:
            compartilhar.append(aluno.publico)

        return compartilhar

    def _procurar_nome(self, atual: str, recebido: str) -> bool:
        return normalizado(recebido) in normalizado(atual)

    def _procurar_email(self, atual: str, recebido: str) -> bool:
        return normalizado(recebido) in normalizado(atual)

    def _procurar_telefone(self, atual: str, recebido: str) -> bool:
        return normalizar_telefone(recebido) == normalizar_telefone(atual)

    def _procurar_codigo_curso(self, atual: int, recebido: int) -> bool:
        return recebido == atual

    def _procurar_prontuario(self, atual: int, recebido: int) -> bool:
        return recebido == atual

    def _casa(self, aluno: AlunoPublico, criterios: dict) -> bool:
        return all(
            self._comparadores[campo](getattr(aluno, campo), procurado)
            for campo, procurado in criterios.items()
        )

    def buscar(self, criterios: dict) -> list[AlunoPublico]:
        invalidos = criterios.keys() - ALUNO_CAMPOS_PUBLICOS
        if invalidos:
            raise ValueError(f"Campos inválidos: {sorted(invalidos)}")

        return [aluno.publico for aluno in self.lista if self._casa(aluno.publico, criterios)]

    def esta_vazio(self) -> bool:
        return len(self.lista) == 0


class CursoTag:
    tag: str

    def __init__(self, nome: str):
        self.tag = self.formatar(nome)

    def formatar(self, nome: str) -> str:
        return normalizado(nome)

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

    def pegar_identificador(self, codigo: int) -> CursoIdentificador | None:
        for curso in self.lista:
            if curso.codigo == codigo:
                return curso.identificador

        return None

    def esta_vazio(self) -> bool:
        return len(self.lista) == 0


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


# Se o curso não existir, perguntar se não deseja criar um com o mesmo nome.
def curso_perguntar_codigo(cursos: Cursos) -> int:
    identificador = CursoIdentificador(leia.string("Digite o nome do curso"))

    if not garantir_curso(cursos, identificador):
        return -1

    codigo = cursos.pegar_codigo(identificador.tag)

    if codigo is None:
        exit(10)

    return codigo


def garantir_curso(cursos: Cursos, identificador: CursoIdentificador) -> bool:
    if cursos.pegar_codigo(identificador.tag):
        return True

    style.erro(f'Não existe nenhum curso chamado "{identificador.nome}"')

    confirmacao = leia.confirmar("Deseja criar um")

    if confirmacao:
        curso_criar(cursos, identificador)

    # TODO: Pedir para o usuário digitar novamente o nome (pode ter sido um erro de digitação).

    return False


# TODO: Antes de concluir, perguntar se não tem nada para mudar
def alunos_cadastrar(alunos: Alunos, cursos: Cursos):
    style.titulo_2("Cadastrar aluno")

    nome = leia.string("Digite o nome completo")
    cpf = leia.cpf()
    telefone = leia.telefone()
    email = leia.email()

    codigo_curso = curso_perguntar_codigo(cursos)

    privado = AlunoPrivado(cpf=cpf)

    publico = AlunoPublico(nome=nome, telefone=telefone, email=email, codigo_curso=codigo_curso)

    alunos.adicionar(privado, publico)

    style.sucesso("Aluno cadastrado")


def alunos_alterar(alunos: Alunos):
    # 1. Qual aluno vai alterar (Busca)?
    # 2. O que vai alterar
    pass


def garantir_aluno(alunos: Alunos, cursos: Cursos) -> bool:
    """
    @return True se há alunos foi cadastrados, False caso contrário.
    """
    if not alunos.esta_vazio():
        return True

    style.erro("Não existe alunos cadastrados")

    confirmacao = leia.confirmar("Deseja cadastar um")

    if confirmacao:
        alunos_cadastrar(alunos, cursos)

    return False


def alunos_buscar(alunos: Alunos, cursos: Cursos):
    buscar_opcoes = {"nome": 1, "email": 2, "telefone": 3, "curso": 4, "prontuario": 5}

    style.titulo_2("Buscando alunos")

    if not garantir_aluno(alunos, cursos):
        return

    opcoes = leia.varias_opcoes_entre(buscar_opcoes)

    if opcoes is None:
        return

    selecionadas = {}

    for opcao in opcoes:
        if opcao == buscar_opcoes["nome"]:
            selecionadas["nome"] = leia.string("Digite o nome")
        elif opcao == buscar_opcoes["email"]:
            selecionadas["email"] = leia.email()
        elif opcao == buscar_opcoes["telefone"]:
            selecionadas["telefone"] = leia.string("Digite o telefone")
        elif opcao == buscar_opcoes["curso"]:
            selecionadas["codigo_curso"] = curso_perguntar_codigo(cursos)
        elif opcao == buscar_opcoes["prontuario"]:
            selecionadas["prontuario"] = leia.inteiro_maior_igual("Digite o prontuário", 0)
        else:
            return

    encontrado = alunos.buscar(selecionadas)

    style.separador()

    if len(encontrado) == 0:
        style.erro("Nenhum resultado foi encontrado")
    else:
        for e in encontrado:
            mostrar_aluno(e, cursos)
        style.sucesso("Busca feita")


def alunos_excluir(alunos: Alunos):
    pass


def mostrar_aluno(aluno: AlunoPublico, cursos: Cursos):
    curso_codigo = aluno.codigo_curso
    curso_ident = cursos.pegar_identificador(curso_codigo)

    if curso_ident is None:
        exit(11)

    style.titulo_3(aluno.nome)
    style.lista(
        [
            f"Email: {aluno.email}",
            f"Telefone: {aluno.telefone}",
            f"Prontuário: {aluno.prontuario}",
            f"Curso: {curso_ident.nome} | {curso_codigo}",
        ]
    )

    style.separador()


def alunos_listar(alunos: Alunos, cursos: Cursos):
    if not garantir_aluno(alunos, cursos):
        return

    style.titulo_2("Listando os alunos")

    compartilhar = alunos.lista_publica()

    for aluno in compartilhar:
        mostrar_aluno(aluno, cursos)


def alunos_menu(alunos: Alunos, cursos: Cursos):
    aluno_opcoes = {"cadastrar": 1, "excluir": 2, "alterar": 3, "buscar": 4, "listar": 5}

    while True:
        style.titulo_1("Aluno")

        opcao = leia.uma_opcao_entre(aluno_opcoes)

        if opcao == aluno_opcoes["cadastrar"]:
            alunos_cadastrar(alunos, cursos)
        elif opcao == aluno_opcoes["alterar"]:
            alunos_alterar(alunos)
        elif opcao == aluno_opcoes["buscar"]:
            alunos_buscar(alunos, cursos)
        elif opcao == aluno_opcoes["excluir"]:
            alunos_excluir(alunos)
        elif opcao == aluno_opcoes["listar"]:
            alunos_listar(alunos, cursos)
        else:
            break


def curso_criar(cursos: Cursos, identificador: CursoIdentificador | None):
    if identificador is None:
        style.titulo_2("Criando novo curso")
        identificador = CursoIdentificador(leia.string("Digite o nome do curso"))
    else:
        style.titulo_2(f'Criando o novo curso "{identificador.nome}"')

    semestres = leia.inteiro_positivo("Quantidade de semestres")

    cursos.adicionar(identificador, semestres)
    style.sucesso("Curso criado")


def curso_mostrar_alunos(cursos):
    pass


def menu_curso(cursos: Cursos):
    curso_opcoes = {
        "alunos": 1,
    }

    while True:
        style.titulo_1("Curso")

        opcao = leia.uma_opcao_entre(curso_opcoes)

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
        style.titulo_1("Disciplina")

        opcao = leia.uma_opcao_entre(disciplina_opcoes)

        if opcao == disciplina_opcoes["buscar_curso"]:
            disciplina_buscar_curso(disciplinas)
        elif opcao == disciplina_opcoes["buscar_semestre"]:
            disciplina_buscar_semestre(disciplinas)
        else:
            break


def menu_principal(alunos: Alunos, cursos: Cursos, disciplinas: Disciplinas):
    area_opcoes: dict[str, int] = {
        "aluno": 1,
        "curso": 2,
        "disciplina": 3,
    }

    while True:
        style.titulo_1("Menu Principal")

        opcao = leia.uma_opcao_entre(area_opcoes)

        if opcao == area_opcoes["aluno"]:
            alunos_menu(alunos, cursos)
        elif opcao == area_opcoes["curso"]:
            menu_curso(cursos)
        elif opcao == area_opcoes["disciplina"]:
            menu_disciplina(disciplinas)
        else:
            break

    style.aviso("Tchau, Tchau!")


def adicionar_cursos_teste(cursos: Cursos):
    cursos.adicionar(identificador=CursoIdentificador("Ciência da Computação"), semestres=8)

    cursos.adicionar(identificador=CursoIdentificador("Pedagogia"), semestres=6)


def adicionar_alunos_teste(alunos: Alunos, cursos: Cursos):
    comp = CursoTag("Ciência da Computação")
    comp_codigo = cursos.pegar_codigo(comp)
    if comp_codigo is None:
        exit(13)

    peda = CursoTag("Pedagogia")
    peda_codigo = cursos.pegar_codigo(peda)
    if peda_codigo is None:
        exit(13)

    alunos.adicionar(
        privado=AlunoPrivado(cpf="123.456.789-10"),
        publico=AlunoPublico(
            nome="Pedro Henrique",
            telefone="(12) 1234-5678",
            email="pedro.henrique@gmail.com",
            codigo_curso=comp_codigo,
        ),
    )

    alunos.adicionar(
        privado=AlunoPrivado(cpf="334.112.789-90"),
        publico=AlunoPublico(
            nome="Ana Luísa",
            telefone="(12) 0987-1234",
            email="ana.lulu@gmail.com",
            codigo_curso=peda_codigo,
        ),
    )


def main():
    alunos = Alunos()
    cursos = Cursos()
    disciplinas = Disciplinas()

    adicionar_cursos_teste(cursos)
    adicionar_alunos_teste(alunos, cursos)

    menu_principal(alunos, cursos, disciplinas)


if __name__ == "__main__":
    main()
