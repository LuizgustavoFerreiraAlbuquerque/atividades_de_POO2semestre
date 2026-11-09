from pathlib import Path
from professor import Professor


class GerenciadorProfessores:
    """Mantém os professores em memória e persiste os dados em professores.txt."""

    def __init__(self, arquivo=None):
        self.arquivo = Path(arquivo) if arquivo else Path(__file__).resolve().parent.parent / "dados" / "professores.txt"
        self.professores = []
        self.arquivo.touch(exist_ok=True)
        self.carregar()

    def carregar(self):
        self.professores = []
        with self.arquivo.open("r", encoding="utf-8") as arquivo:
            for numero_linha, linha in enumerate(arquivo, start=1):
                linha = linha.rstrip("\n")
                if not linha:
                    continue
                partes = linha.split(";")
                if len(partes) != 4:
                    print(f"Aviso: linha {numero_linha} inválida em {self.arquivo}.")
                    continue
                codigo, nome, cpf, especialidade = partes
                self.professores.append(Professor(codigo, nome, cpf, especialidade))

    def salvar(self):
        with self.arquivo.open("w", encoding="utf-8") as arquivo:
            for p in self.professores:
                campos = [p.codigo, p.nome, p.cpf, p.especialidade]
                if any(";" in campo or "\n" in campo for campo in campos):
                    raise ValueError("Os campos não podem conter ponto e vírgula ou quebra de linha.")
                arquivo.write(";".join(campos) + "\n")

    def pesquisar(self, termo):
        termo = str(termo).strip().casefold()
        return [
            p for p in self.professores
            if p.codigo.casefold() == termo or termo in p.nome.casefold()
        ]

    def cadastrar(self, codigo, nome, cpf, especialidade):
        if not all(str(v).strip() for v in (codigo, nome, cpf, especialidade)):
            raise ValueError("Preencha todos os campos do professor.")
        if self.pesquisar_codigo(codigo):
            raise ValueError("Já existe um professor com esse código.")
        professor = Professor(codigo, nome, cpf, especialidade)
        self.professores.append(professor)
        self.salvar()
        return professor

    def pesquisar_codigo(self, codigo):
        codigo = str(codigo).strip()
        for p in self.professores:
            if p.codigo == codigo:
                return p
        return None

    def alterar(self, codigo, nome, cpf, especialidade):
        professor = self.pesquisar_codigo(codigo)
        if professor is None:
            raise ValueError("Professor não encontrado.")
        if not all(str(v).strip() for v in (nome, cpf, especialidade)):
            raise ValueError("Preencha todos os campos do professor.")
        professor.nome = str(nome).strip()
        professor.cpf = str(cpf).strip()
        professor.especialidade = str(especialidade).strip()
        self.salvar()
        return professor

    def excluir(self, codigo):
        professor = self.pesquisar_codigo(codigo)
        if professor is None:
            raise ValueError("Professor não encontrado.")
        self.professores.remove(professor)
        self.salvar()
