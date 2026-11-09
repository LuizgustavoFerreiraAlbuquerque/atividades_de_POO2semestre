from pathlib import Path
from disciplina import Disciplina


class GerenciadorDisciplinas:
    """Mantém disciplinas em memória e persiste os dados em disciplinas.txt."""

    def __init__(self, arquivo=None):
        self.arquivo = Path(arquivo) if arquivo else Path(__file__).resolve().parent.parent / "dados" / "disciplinas.txt"
        self.disciplinas = []
        self.arquivo.touch(exist_ok=True)
        self.carregar()

    def carregar(self):
        self.disciplinas = []
        with self.arquivo.open("r", encoding="utf-8") as arquivo:
            for numero_linha, linha in enumerate(arquivo, start=1):
                linha = linha.rstrip("\n")
                if not linha:
                    continue
                partes = linha.split(";")
                if len(partes) != 5:
                    print(f"Aviso: linha {numero_linha} inválida em {self.arquivo}.")
                    continue
                codigo, nome, carga, codigo_professor, codigo_curso = partes
                try:
                    self.disciplinas.append(
                        Disciplina(codigo, nome, int(carga), codigo_professor, codigo_curso)
                    )
                except ValueError:
                    print(f"Aviso: carga horária inválida na linha {numero_linha}.")

    def salvar(self):
        with self.arquivo.open("w", encoding="utf-8") as arquivo:
            for d in self.disciplinas:
                campos = [
                    d.codigo, d.nome, str(d.carga_horaria),
                    d.codigo_professor, d.codigo_curso
                ]
                if any(";" in campo or "\n" in campo for campo in campos):
                    raise ValueError("Os campos não podem conter ponto e vírgula ou quebra de linha.")
                arquivo.write(";".join(campos) + "\n")

    def pesquisar_codigo(self, codigo):
        codigo = str(codigo).strip()
        for d in self.disciplinas:
            if d.codigo == codigo:
                return d
        return None

    def pesquisar(self, termo):
        termo = str(termo).strip().casefold()
        return [
            d for d in self.disciplinas
            if d.codigo.casefold() == termo or termo in d.nome.casefold()
        ]

    def cadastrar(self, codigo, nome, carga_horaria, codigo_professor, codigo_curso,
                  gerenciador_professores=None, gerenciador_cursos=None):
        if not all(str(v).strip() for v in
                   (codigo, nome, carga_horaria, codigo_professor, codigo_curso)):
            raise ValueError("Preencha todos os campos da disciplina.")
        if self.pesquisar_codigo(codigo):
            raise ValueError("Já existe uma disciplina com esse código.")
        try:
            carga = int(carga_horaria)
        except (TypeError, ValueError):
            raise ValueError("A carga horária deve ser um número inteiro.")
        if carga <= 0:
            raise ValueError("A carga horária deve ser maior que zero.")
        if gerenciador_professores is not None:
            if not gerenciador_professores.pesquisar_codigo(codigo_professor):
                raise ValueError("O código do professor não está cadastrado.")
        if gerenciador_cursos is not None:
            if not gerenciador_cursos.pesquisar(codigo_curso):
                raise ValueError("O código do curso não está cadastrado.")
        disciplina = Disciplina(codigo, nome, carga, codigo_professor, codigo_curso)
        self.disciplinas.append(disciplina)
        self.salvar()
        return disciplina

    def alterar(self, codigo, nome, carga_horaria, codigo_professor, codigo_curso,
                gerenciador_professores=None, gerenciador_cursos=None):
        disciplina = self.pesquisar_codigo(codigo)
        if disciplina is None:
            raise ValueError("Disciplina não encontrada.")
        if not all(str(v).strip() for v in
                   (nome, carga_horaria, codigo_professor, codigo_curso)):
            raise ValueError("Preencha todos os campos da disciplina.")
        try:
            carga = int(carga_horaria)
        except (TypeError, ValueError):
            raise ValueError("A carga horária deve ser um número inteiro.")
        if carga <= 0:
            raise ValueError("A carga horária deve ser maior que zero.")
        if gerenciador_professores is not None:
            if not gerenciador_professores.pesquisar_codigo(codigo_professor):
                raise ValueError("O código do professor não está cadastrado.")
        if gerenciador_cursos is not None:
            if not gerenciador_cursos.pesquisar(codigo_curso):
                raise ValueError("O código do curso não está cadastrado.")
        disciplina.nome = str(nome).strip()
        disciplina.carga_horaria = carga
        disciplina.codigo_professor = str(codigo_professor).strip()
        disciplina.codigo_curso = str(codigo_curso).strip()
        self.salvar()
        return disciplina

    def excluir(self, codigo):
        disciplina = self.pesquisar_codigo(codigo)
        if disciplina is None:
            raise ValueError("Disciplina não encontrada.")
        self.disciplinas.remove(disciplina)
        self.salvar()
