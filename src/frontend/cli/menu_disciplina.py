from sistema.modelos.disciplina import Disciplinas

from . import leia, mostre


def disciplina_buscar_curso(disciplinas: Disciplinas):
    pass


def disciplina_buscar_semestre(disciplinas: Disciplinas):
    pass


def menu_principal(disciplinas: Disciplinas):
    disciplina_opcoes = {"buscar_semestre": 1, "buscar_curso": 2}

    while True:
        mostre.titulo_1("Disciplina")

        opcao = leia.uma_opcao_entre(disciplina_opcoes)

        if opcao == disciplina_opcoes["buscar_curso"]:
            disciplina_buscar_curso(disciplinas)
        elif opcao == disciplina_opcoes["buscar_semestre"]:
            disciplina_buscar_semestre(disciplinas)
        else:
            break
