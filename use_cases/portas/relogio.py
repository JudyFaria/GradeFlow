from datetime import date
from typing import Protocol


class Relogio(Protocol):
    """Fornece a data atual; a data entra no domínio só por injeção."""

    def hoje(self) -> date: ...
