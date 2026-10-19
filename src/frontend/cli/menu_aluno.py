from sistema.modelos.aluno import AlunoPrivado, AlunoPublico, Alunos
from sistema.modelos.curso import Cursos, CursoTag

from . import erros, leia, menu_curso, mostre


def garantir_aluno(alunos: Alunos, cursos: Cursos) -> bool:
    """
    @return True se há alunos foi cadastrados, False caso contrário.
    """
    if not alunos.esta_vazio():
        return True

    mostre.erro("Não existe alunos cadastrados.")

    confirmacao = leia.confirmar("Deseja cadastar um?")

    if confirmacao:
        menu_cadastrar(alunos, cursos)

    return False


def mostrar_aluno(aluno: AlunoPublico, cursos: Cursos, indice: int):
    curso_codigo = aluno.codigo_curso
    curso_ident = cursos.pegar_identificador(curso_codigo)

    if curso_ident is None:
        exit(11)

    mostre.titulo_3(f"{indice}. {aluno.nome}")
    mostre.lista(
        [
            f"Email: {aluno.email}",
            f"Telefone: {aluno.telefone}",
            f"Prontuário: {aluno.prontuario}",
            f"Curso: {curso_ident.nome} | {curso_codigo}",
        ]
    )

    mostre.separador()


def mostrar_alunos(alunos: list[AlunoPublico], cursos: Cursos):
    for indice, aluno in enumerate(alunos):
        mostrar_aluno(aluno, cursos, indice + 1)


def perguntar_campos_publicos(alunos: Alunos, cursos: Cursos) -> dict:
    buscar_opcoes = {"nome": 1, "email": 2, "telefone": 3, "curso_codigo": 4}

    if not garantir_aluno(alunos, cursos):
        raise erros.OperaçãoCanceladaError

    opcoes = leia.varias_opcoes_entre(buscar_opcoes)

    alterar = {}

    for opcao in opcoes:
        if opcao == buscar_opcoes["nome"]:
            alterar["nome"] = leia.string("Digite o nome.")
        elif opcao == buscar_opcoes["email"]:
            alterar["email"] = leia.email()
        elif opcao == buscar_opcoes["telefone"]:
            alterar["telefone"] = leia.telefone()
        elif opcao == buscar_opcoes["nome_curso"]:
            alterar["curso_codigo"] = menu_curso.perguntar_codigo(cursos)
        else:
            raise erros.OperaçãoCanceladaError

    return alterar


# Não verifica se os dados são válidos!
def perguntar_busca(alunos: Alunos, cursos: Cursos) -> dict:
    buscar_opcoes = {"nome": 1, "email": 2, "telefone": 3, "nome_curso": 4, "prontuario": 5}

    if not garantir_aluno(alunos, cursos):
        raise erros.OperaçãoCanceladaError

    opcoes = leia.varias_opcoes_entre(buscar_opcoes)

    criterios = alunos.criterios_vazio()

    for opcao in opcoes:
        if opcao == buscar_opcoes["nome"]:
            criterios["nome"] = leia.string("Digite o nome.")
        elif opcao == buscar_opcoes["email"]:
            criterios["email"] = leia.string("Digite o email.")
        elif opcao == buscar_opcoes["telefone"]:
            criterios["telefone"] = leia.string("Digite o telefone.")
        elif opcao == buscar_opcoes["nome_curso"]:
            tag = CursoTag(leia.string("Digite o nome do curso."))
            criterios["curso_tag"] = tag
        elif opcao == buscar_opcoes["prontuario"]:
            criterios["prontuario"] = leia.inteiro_maior_igual("Digite o prontuário", 0)
        else:
            raise erros.OperaçãoCanceladaError

    return criterios


def buscar(alunos: Alunos, cursos: Cursos) -> list[AlunoPublico]:
    criterios = perguntar_busca(alunos, cursos)

    return alunos.buscar(criterios, cursos)


def buscar_melhor(alunos: Alunos, cursos: Cursos) -> list[AlunoPublico]:
    while True:
        resuldados = buscar(alunos, cursos)

        if len(resuldados) == 0:
            mostre.erro("Nenhum resultado foi encontrado.")

            confirmacao = leia.confirmar("Deseja procurar novamente.")

            if not confirmacao:
                raise erros.OperaçãoCanceladaError

            continue

        return resuldados


def escolher_um_aluno(alunos: Alunos, cursos: Cursos) -> AlunoPublico:
    while True:
        resuldados = buscar_melhor(alunos, cursos)

        if len(resuldados) == 1:
            aluno = resuldados[0]
            mostrar_aluno(aluno, cursos, 1)
            confirmacao = leia.confirmar("Deseja alterar esse aluno?")

            if confirmacao:
                return aluno
            else:
                confirmacao = leia.confirmar("Procurar denovo?")
                if confirmacao:
                    continue
                else:
                    raise erros.OperaçãoCanceladaError

        mostre.aviso("Mais de um aluno foi encontrado.")
        mostrar_alunos(resuldados, cursos)

        opcao = leia.inteiro_entre("Selecione qual deve alterar.", len(resuldados) + 1)

        if opcao == 0:
            raise erros.OperaçãoCanceladaError

        indice = opcao - 1

        return resuldados[indice]


def alterar_publico(publico: AlunoPublico, alunos: Alunos, cursos: Cursos):
    mostre.mensagem("Quais campos deseja alterar?")
    alterar = perguntar_campos_publicos(alunos, cursos)

    alunos.alterar(publico, alterar)


def alterar_privado():
    pass


def menu_cadastrar(alunos: Alunos, cursos: Cursos):
    mostre.titulo_2("Cadastrar aluno")

    nome = leia.string("Digite o nome completo.")
    cpf = leia.cpf()
    telefone = leia.telefone()
    email = leia.email()

    codigo = menu_curso.perguntar_codigo(cursos)

    if codigo is None:
        mostre.erro("Não é possível cadastrar um aluno sem curso.")
        return

    privado = AlunoPrivado(cpf=cpf)

    publico = AlunoPublico(nome=nome, telefone=telefone, email=email, codigo_curso=codigo)

    alunos.adicionar(privado, publico)

    mostre.sucesso("Aluno cadastrado.")


def menu_alterar(alunos: Alunos, cursos: Cursos):
    mostre.titulo_2("Alterar aluno")

    mostre.mensagem("Procure o aluno que deseja alterar.")

    try:
        selecionado = escolher_um_aluno(alunos, cursos)
    except erros.OperaçãoCanceladaError:
        return

    # quer_alterar_privado = leia.confirmar("Deseja alterar os dados privados.")

    alterar_publico(selecionado, alunos, cursos)

    # if quer_alterar_privado:
    #     alterar_privado()


def menu_buscar(alunos: Alunos, cursos: Cursos):
    mostre.titulo_2("Buscando alunos")

    mostre.mensagem("Deseja buscar por quais critérios?")
    try:
        encontrados = buscar_melhor(alunos, cursos)
    except erros.OperaçãoCanceladaError:
        return

    mostre.separador()

    for indice, aluno in enumerate(encontrados):
        mostrar_aluno(aluno, cursos, indice)

    mostre.sucesso("Busca feita.")


def menu_excluir(alunos: Alunos):
    pass


def menu_listar(alunos: Alunos, cursos: Cursos):
    if not garantir_aluno(alunos, cursos):
        return

    mostre.titulo_2("Listando os alunos")

    compartilhar = alunos.lista_publica()

    mostrar_alunos(compartilhar, cursos)


def menu_principal(alunos: Alunos, cursos: Cursos):
    aluno_opcoes = {"cadastrar": 1, "excluir": 2, "alterar": 3, "buscar": 4, "listar": 5}

    while True:
        mostre.titulo_1("Aluno")

        opcao = leia.uma_opcao_entre(aluno_opcoes)

        if opcao == aluno_opcoes["cadastrar"]:
            menu_cadastrar(alunos, cursos)
        elif opcao == aluno_opcoes["alterar"]:
            menu_alterar(alunos, cursos)
        elif opcao == aluno_opcoes["buscar"]:
            menu_buscar(alunos, cursos)
        elif opcao == aluno_opcoes["excluir"]:
            menu_excluir(alunos)
        elif opcao == aluno_opcoes["listar"]:
            menu_listar(alunos, cursos)
        else:
            break
