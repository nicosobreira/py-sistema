from sistema.banco.alunos import Alunos
from sistema.banco.cursos import Cursos
from sistema.banco.disciplinas import Disciplinas

from .. import leia, style
from .alunos import alunos_menu
from .cursos import menu_curso
from .disciplinas import menu_disciplina


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
