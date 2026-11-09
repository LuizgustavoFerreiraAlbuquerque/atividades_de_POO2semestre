class Aluno:
    def __init__(self, matricula, nome, cpf, email, codigo_curso):
        self._matricula = matricula
        self._nome = nome
        self._cpf = cpf
        self._email = email
        self._codigo_curso = codigo_curso

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, valor):
        self._matricula = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        self._cpf = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = valor

    @property
    def codigo_curso(self):
        return self._codigo_curso

    @codigo_curso.setter
    def codigo_curso(self, valor):
        self._codigo_curso = valor

    def __str__(self):
        return (
            f"Matrícula: {self.matricula} | Nome: {self.nome} | "
            f"CPF: {self.cpf} | E-mail: {self.email} | "
            f"Código do curso: {self.codigo_curso}"
        )


    