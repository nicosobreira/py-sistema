from sistema.modelos.curso import CursoIdentificador, Cursos

from . import leia, mostre


# Se o curso não existir, perguntar se não deseja criar um com o mesmo nome.
def perguntar_codigo(cursos: Cursos) -> int | None:
    identificador = perguntar_curso(cursos)

    if identificador is None:
        return None

    codigo = cursos.pegar_codigo(identificador.tag)

    return codigo


def perguntar_curso(cursos: Cursos) -> CursoIdentificador | None:
    identificador = CursoIdentificador(leia.string("Digite o nome do curso."))

    codigo = cursos.pegar_codigo(identificador.tag)

    if codigo is None:
        mostre.erro(f'Não existe nenhum curso chamado "{identificador.nome}".')

        confirmacao = leia.confirmar("Deseja criar um?")
        if not confirmacao:
            return None

        curso_criar(cursos, identificador)

    return identificador


def garantir_curso(cursos: Cursos, identificador: CursoIdentificador) -> bool:
    if cursos.pegar_codigo(identificador.tag):
        return True

    mostre.erro(f'Não existe nenhum curso chamado "{identificador.nome}"')

    confirmacao = leia.confirmar("Deseja criar um?")

    if confirmacao:
        curso_criar(cursos, identificador)

    # TODO: Pedir para o usuário digitar novamente o nome (pode ter sido um erro de digitação).

    return False


# TODO: Antes de concluir, perguntar se não tem nada para mudar


def curso_criar(cursos: Cursos, identificador: CursoIdentificador | None):
    if identificador is None:
        mostre.titulo_2("Criando novo curso")
        identificador = CursoIdentificador(leia.string("Digite o nome do curso."))
    else:
        mostre.titulo_2(f'Criando o novo curso "{identificador.nome}"')

    semestres = leia.inteiro_positivo("Quantidade de semestres.")

    cursos.adicionar(identificador, semestres)
    mostre.sucesso("Curso criado.")


def curso_mostrar_alunos(cursos):
    pass


def menu_principal(cursos: Cursos):
    curso_opcoes = {
        "alunos": 1,
    }

    while True:
        mostre.titulo_1("Curso")

        opcao = leia.uma_opcao_entre(curso_opcoes)

        if opcao == curso_opcoes["alunos"]:
            curso_mostrar_alunos(cursos)
        else:
            break
