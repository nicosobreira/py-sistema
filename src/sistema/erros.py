# TODO: Adicionar mais erros de cadastros, como entrada maior que o esperado.


class CursoInexistenteError(Exception):
    pass


class CadastroError(Exception):
    pass


class CpfInvalidoError(CadastroError):
    pass
