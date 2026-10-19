import frontend.cli.menu_principal as menu_principal
from sistema.modelos.aluno import AlunoPrivado, AlunoPublico, Alunos
from sistema.modelos.curso import CursoIdentificador, Cursos, CursoTag
from sistema.modelos.disciplina import Disciplinas
from sistema.tipos.cpf import Cpf
from sistema.tipos.email import Email
from sistema.tipos.telefone import Telefone

# TODO: Adicionar um formulario com setinhas, mais parecido com um TUI.

# TODO: Adicionar um sistema de verificação de "má digitação", apartir da função
# `def verificar(match: str, possiveis: list[str]) -> str`.
# Cada string vai receber uma porcentagem de 0 a 100% do quão próximo ela está de match.
# Retornar o valor de maior porcentagem.


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
        privado=AlunoPrivado(cpf=Cpf("123.456.789-10")),
        publico=AlunoPublico(
            nome="Pedro Henrique",
            telefone=Telefone("(12) 1234-5678"),
            email=Email("pedro.henrique@gmail.com"),
            codigo_curso=comp_codigo,
        ),
    )

    alunos.adicionar(
        privado=AlunoPrivado(cpf=Cpf("334.112.789-90")),
        publico=AlunoPublico(
            nome="Ana Luísa",
            telefone=Telefone("(12) 0987-1234"),
            email=Email("ana.lulu@gmail.com"),
            codigo_curso=peda_codigo,
        ),
    )


def main():
    alunos = Alunos()
    cursos = Cursos()
    disciplinas = Disciplinas()

    adicionar_cursos_teste(cursos)
    adicionar_alunos_teste(alunos, cursos)

    menu_principal.menu_principal(alunos, cursos, disciplinas)


if __name__ == "__main__":
    main()
