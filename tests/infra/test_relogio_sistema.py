from datetime import date

from infra.relogio_sistema import RelogioSistema


def test_hoje_devolve_a_data_do_sistema():
    assert RelogioSistema().hoje() == date.today()
