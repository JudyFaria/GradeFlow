from domain.erros import ErroDeDominio


def test_erro_de_dominio_e_uma_excecao():
    assert issubclass(ErroDeDominio, Exception)


def test_erro_de_dominio_guarda_a_mensagem_informada():
    erro = ErroDeDominio("Precisa vir depois de INF1007")

    assert str(erro) == "Precisa vir depois de INF1007"


def test_erro_especifico_derivado_e_capturado_como_erro_de_dominio():
    class ErroEspecifico(ErroDeDominio):
        pass

    try:
        raise ErroEspecifico("falhou")
    except ErroDeDominio as erro:
        assert str(erro) == "falhou"


def test_erro_nao_encontrado_e_um_erro_de_dominio_com_a_mensagem():
    from domain.erros import ErroNaoEncontrado

    erro = ErroNaoEncontrado("Planejamento não encontrado")

    assert isinstance(erro, ErroDeDominio)
    assert str(erro) == "Planejamento não encontrado"
