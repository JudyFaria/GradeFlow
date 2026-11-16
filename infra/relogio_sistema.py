from datetime import date


class RelogioSistema:
    """Implementa a porta `Relogio` com a data do sistema."""

    def hoje(self) -> date:
        return date.today()
