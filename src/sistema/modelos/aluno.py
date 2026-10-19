from dataclasses import dataclass

import utils
from sistema.tipos.cpf import Cpf
from sistema.tipos.email import Email
from sistema.tipos.telefone import Telefone

from .curso import Cursos, CursoTag


@dataclass
class AlunoPublico:
    codigo_curso: int
    nome: str
    email: Email
    telefone: Telefone
    prontuario: int = -1


@dataclass
class AlunoPrivado:
    cpf: Cpf


@dataclass
class Aluno:
    privado: AlunoPrivado
    publico: AlunoPublico


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
            "curso_tag": self._procurar_curso_tag,
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
        return utils.normalizado(recebido) in utils.normalizado(atual)

    def _procurar_email(self, atual: str, recebido: str) -> bool:
        return utils.normalizado(recebido) in utils.normalizado(atual)

    def _procurar_telefone(self, atual: str, recebido: str) -> bool:
        return Telefone.normalizar(recebido) in Telefone.normalizar(atual)

    def _procurar_curso_tag(self, atual: CursoTag, recebido: CursoTag) -> bool:
        return recebido.tag in atual.tag

    def _procurar_prontuario(self, atual: int, recebido: int) -> bool:
        return recebido == atual

    def _casa(self, aluno: dict, criterios: dict) -> bool:
        return all(
            self._comparadores[campo](aluno[campo], procurado)
            for campo, procurado in criterios.items()
            if procurado is not None
        )

    def buscar(self, criterios: dict, cursos: Cursos) -> list[AlunoPublico]:
        invalidos = criterios.keys() - self.criterios_vazio()

        if invalidos:
            raise ValueError(f"Campos inválidos: {sorted(invalidos)}")

        return [
            aluno.publico
            for aluno in self.lista
            if self._casa(self._aluno_para_busca(aluno.publico, cursos), criterios)
        ]

    def esta_vazio(self) -> bool:
        return len(self.lista) == 0

    def alterar(self, publico: AlunoPublico, alterar: dict):
        invalidos = alterar.keys() - self.alterar_vazio()
        if invalidos:
            raise ValueError(f"Campos inválidos: {sorted(invalidos)}")

        novo_aluno = AlunoPublico(
            nome=if alterar.nome is not None alterar.nome else publico.nome,
            telefone=alterar.telefone  if alterar.telefone is not None,
            email=alterar.email  if alterar.email is not None,
            prontuario=publico.prontuario,
            codigo_curso=alterar.codigo_curso,
        )

    @staticmethod
    def _aluno_para_busca(aluno: AlunoPublico, cursos: Cursos) -> dict:
        tag = cursos.pegar_tag(aluno.codigo_curso)

        if tag is None:
            exit(10)

        return {
            "nome": aluno.nome,
            "email": aluno.email.__str__(),
            "telefone": aluno.telefone.__str__(),
            "curso_tag": tag,
            "prontuario": aluno.prontuario,
        }

    @staticmethod
    def criterios_vazio() -> dict:
        return {
            "nome": None,
            "email": None,
            "telefone": None,
            "curso_tag": None,
            "prontuario": None,
        }

    @staticmethod
    def alterar_vazio() -> dict:
        return {
            "nome": None,
            "email": None,
            "telefone": None,
            "curso_codigo": None,
        }
