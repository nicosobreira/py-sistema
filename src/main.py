from sistema.banco.cursos import Cursos
from sistema.banco.disciplinas import Disciplinas
from sistema.tipos.aluno import AlunoPrivado, AlunoPublico
from sistema.tipos.curso import CursoIdentificador, CursoTag

from interface.cli.menus.principal import menu_principal
from sistema.armazenamento import *


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
