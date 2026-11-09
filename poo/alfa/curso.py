class Curso:
    def __init__(self, codigo, nome, modalidade):
        self._codigo = codigo
        self._nome = nome
        self._modalidade = modalidade

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def modalidade(self):
        return self._modalidade

    @modalidade.setter
    def modalidade(self, valor):
        self._modalidade = valor

    def __str__(self):
        return (
            f"Código: {self.codigo} | Nome: {self.nome} | "
            f"Modalidade: {self.modalidade}"
        )