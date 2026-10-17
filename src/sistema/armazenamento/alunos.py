import sistema.formatacao as format
from sistema.tipos.aluno import ALUNO_CAMPOS_PUBLICOS, Aluno, AlunoPrivado, AlunoPublico


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
            "codigo_curso": self._procurar_codigo_curso,
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
        return format.normalizar(recebido) in format.normalizar(atual)

    def _procurar_email(self, atual: str, recebido: str) -> bool:
        return format.normalizar(recebido) in format.normalizar(atual)

    def _procurar_telefone(self, atual: str, recebido: str) -> bool:
        return format.normalizar_telefone(recebido) == format.normalizar_telefone(atual)

    def _procurar_codigo_curso(self, atual: int, recebido: int) -> bool:
        return recebido == atual

    def _procurar_prontuario(self, atual: int, recebido: int) -> bool:
        return recebido == atual

    def _casa(self, aluno: AlunoPublico, criterios: dict) -> bool:
        return all(
            self._comparadores[campo](getattr(aluno, campo), procurado)
            for campo, procurado in criterios.items()
        )

    def buscar(self, criterios: dict) -> list[AlunoPublico]:
        invalidos = criterios.keys() - ALUNO_CAMPOS_PUBLICOS
        if invalidos:
            raise ValueError(f"Campos inválidos: {sorted(invalidos)}")

        return [aluno.publico for aluno in self.lista if self._casa(aluno.publico, criterios)]

    def esta_vazio(self) -> bool:
        return len(self.lista) == 0
