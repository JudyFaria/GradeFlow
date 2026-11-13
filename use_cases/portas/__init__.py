"""Portas (interfaces de repositório) consumidas pelos casos de uso.

Convenção: uma porta pequena por necessidade, em módulo próprio, como
`typing.Protocol`. Cada caso de uso recebe suas portas no `__init__` e
expõe um único método público, `executar`. As implementações concretas
ficam em `infra/repositories/`; os falsos em memória, em `tests/`.
"""
