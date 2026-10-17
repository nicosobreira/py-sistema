from sistema.banco.cursos import Cursos
from sistema.tipos.curso import CursoIdentificador

from .. import leia, style


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
