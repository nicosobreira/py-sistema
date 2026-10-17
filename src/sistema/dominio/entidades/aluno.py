from dataclasses import dataclass, fields


@dataclass
class AlunoPublico:
    codigo_curso: int
    nome: str
    email: str
    telefone: str
    prontuario: int = -1


@dataclass
class AlunoPrivado:
    cpf: str


@dataclass
class Aluno:
    privado: AlunoPrivado
    publico: AlunoPublico


ALUNO_CAMPOS_PUBLICOS = {f.name for f in fields(AlunoPublico)}
