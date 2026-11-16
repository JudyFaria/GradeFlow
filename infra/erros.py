"""Erros de infraestrutura. Não são erros de domínio: viram 500 genérico."""


class ErroDeConfiguracao(Exception):
    """Configuração obrigatória ausente (ex.: variável de ambiente)."""


class ErroDeInfraestrutura(Exception):
    """Falha de recurso externo, sem detalhes sensíveis na mensagem."""


class ErroDeMigracao(Exception):
    """Uma migração falhou e foi desfeita."""
