class Disciplina:
    """Representa uma disciplina, usando atributos protegidos e propriedades."""

    def __init__(self, codigo, nome, carga_horaria, codigo_professor, codigo_curso):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.codigo_professor = codigo_professor
        self.codigo_curso = codigo_curso

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
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        self._carga_horaria = int(valor)

    @property
    def codigo_professor(self):
        return self._codigo_professor

    @codigo_professor.setter
    def codigo_professor(self, valor):
        self._codigo_professor = str(valor).strip()

    @property
    def codigo_curso(self):
        return self._codigo_curso

    @codigo_curso.setter
    def codigo_curso(self, valor):
        self._codigo_curso = str(valor).strip()

    def __str__(self):
        return (
            f"Código: {self.codigo} | Nome: {self.nome} | "
            f"Carga horária: {self.carga_horaria}h | "
            f"Código do professor: {self.codigo_professor} | "
            f"Código do curso: {self.codigo_curso}"
        )
