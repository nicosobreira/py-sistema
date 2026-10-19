from sistema.modelos.aluno import Alunos
from sistema.modelos.curso import Cursos
from sistema.modelos.disciplina import Disciplinas

from . import leia, menu_aluno, menu_curso, menu_disciplina, mostre


def menu_principal(alunos: Alunos, cursos: Cursos, disciplinas: Disciplinas):
    area_opcoes: dict[str, int] = {
        "aluno": 1,
        "curso": 2,
        "disciplina": 3,
    }

    while True:
        mostre.titulo_1("Menu Principal")

        opcao = leia.uma_opcao_entre(area_opcoes)

        if opcao == area_opcoes["aluno"]:
            menu_aluno.menu_principal(alunos, cursos)
        elif opcao == area_opcoes["curso"]:
            menu_curso.menu_principal(cursos)
        elif opcao == area_opcoes["disciplina"]:
            menu_disciplina.menu_principal(disciplinas)
        else:
            break

    mostre.aviso("Tchau, Tchau!")
