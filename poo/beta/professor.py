class Professor:
    """Representa um professor, usando atributos protegidos e propriedades."""

    def __init__(self, codigo, nome, cpf, especialidade):
        self.codigo = codigo
        self.nome = nome
        self.cpf = cpf
        self.especialidade = especialidade

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = str(valor).strip()

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = str(valor).strip()

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        self._cpf = str(valor).strip()

    @property
    def especialidade(self):
        return self._especialidade

    @especialidade.setter
    def especialidade(self, valor):
        self._especialidade = str(valor).strip()

    def __str__(self):
        return (
            f"Código: {self.codigo} | Nome: {self.nome} | "
            f"CPF: {self.cpf} | Especialidade: {self.especialidade}"
        )
