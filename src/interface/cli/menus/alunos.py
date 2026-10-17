from sistema.banco.alunos import Alunos
from sistema.banco.cursos import Cursos
from sistema.tipos.aluno import AlunoPrivado, AlunoPublico

from .. import leia, style
from . import cursos as cur


# TODO: Antes de concluir, perguntar se não tem nada para mudar
def alunos_cadastrar(alunos: Alunos, cursos: Cursos):
    style.titulo_2("Cadastrar aluno")

    nome = leia.string("Digite o nome completo")
    cpf = leia.cpf()
    telefone = leia.telefone()
    email = leia.email()

    codigo_curso = cur.curso_perguntar_codigo(cursos)

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
            selecionadas["codigo_curso"] = cur.curso_perguntar_codigo(cursos)
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
