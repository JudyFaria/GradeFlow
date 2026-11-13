class ErroDeDominio(Exception):
    """Raiz de todos os erros de regra de negócio.

    O mapeamento para HTTP fica em app/, nunca aqui.
    """


class ErroNaoEncontrado(ErroDeDominio):
    """Recurso inexistente ou pertencente a outro aluno.

    Os dois casos são indistinguíveis de propósito (privacidade).
    """
