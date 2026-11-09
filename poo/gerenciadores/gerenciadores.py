"""Gerenciadores com CRUD, carregamento e persistência em arquivos TXT."""
from pathlib import Path
from modelos.entidades import Aluno, Curso, Professor, Disciplina

BASE = Path(__file__).resolve().parent.parent
DADOS = BASE / "dados"
DADOS.mkdir(exist_ok=True)

class GerenciadorBase:
    modelo = None
    arquivo_nome = ""
    campos = ()
    identificador = ""

    def __init__(self):
        self.arquivo = DADOS / self.arquivo_nome
        self.arquivo.touch(exist_ok=True)
        self.registros = []
        self.carregar()

    def carregar(self):
        """RF11: carrega os registros do TXT para objetos na memória."""
        self.registros = []
        with self.arquivo.open("r", encoding="utf-8") as f:
            for numero, linha in enumerate(f, 1):
                linha = linha.rstrip("\n")
                if not linha:
                    continue
                partes = linha.split(";")
                if len(partes) != len(self.campos):
                    print(f"Aviso: linha {numero} ignorada em {self.arquivo_nome} (quantidade de campos inválida).")
                    continue
                valores = dict(zip(self.campos, partes))
                try:
                    if self.modelo is Disciplina:
                        valores["carga_horaria"] = int(valores["carga_horaria"])
                    self.registros.append(self.modelo(**valores))
                except (TypeError, ValueError):
                    print(f"Aviso: linha {numero} inválida em {self.arquivo_nome}.")

    def salvar(self):
        """RF10/RF12: regrava o arquivo TXT usando ponto e vírgula."""
        with self.arquivo.open("w", encoding="utf-8") as f:
            for obj in self.registros:
                valores = []
                for campo in self.campos:
                    valor = str(getattr(obj, campo))
                    if ";" in valor or "\n" in valor or "\r" in valor:
                        raise ValueError("Os campos não podem conter ponto e vírgula ou quebra de linha.")
                    valores.append(valor)
                f.write(";".join(valores) + "\n")

    def codigo(self, obj):
        return str(getattr(obj, self.identificador))

    def pesquisar(self, termo):
        """RF03: pesquisa por identificador ou parte do nome."""
        termo = str(termo).strip().casefold()
        return [o for o in self.registros if self.codigo(o).casefold() == termo or termo in str(o.nome).casefold()]

    def obter(self, identificador):
        chave = str(identificador).strip()
        return next((o for o in self.registros if self.codigo(o) == chave), None)

    def cadastrar(self, **dados):
        """RF01: valida campos, cria objeto e persiste."""
        dados = {k: str(v).strip() if k != "carga_horaria" else v for k, v in dados.items()}
        if any(v is None or not str(v).strip() for v in dados.values()):
            raise ValueError("Todos os campos são obrigatórios.")
        if any(";" in str(v) or "\n" in str(v) or "\r" in str(v) for v in dados.values()):
            raise ValueError("Não use ponto e vírgula ou quebra de linha nos campos.")
        chave = str(dados[self.identificador]).strip()
        if self.obter(chave):
            raise ValueError(f"Já existe um registro com identificador {chave}.")
        if self.modelo is Curso:
            modalidade = str(dados["modalidade"]).strip().upper()
            if modalidade not in ("PRESENCIAL", "EAD"):
                raise ValueError("Modalidade deve ser Presencial ou EAD.")
            dados["modalidade"] = "Presencial" if modalidade == "PRESENCIAL" else "EAD"
        if self.modelo is Disciplina:
            try:
                dados["carga_horaria"] = int(dados["carga_horaria"])
            except (ValueError, TypeError):
                raise ValueError("Carga horária deve ser um número inteiro.")
            if dados["carga_horaria"] <= 0:
                raise ValueError("Carga horária deve ser maior que zero.")
        self.validar_relacionamentos(dados)
        obj = self.modelo(**dados)
        self.registros.append(obj)
        self.salvar()
        return obj

    def validar_relacionamentos(self, dados):
        """Subclasses específicas validam chaves estrangeiras."""

    def alterar(self, identificador, **alteracoes):
        """RF04: altera atributos mantendo o identificador único."""
        obj = self.obter(identificador)
        if obj is None:
            raise ValueError("Registro não encontrado.")
        dados = {campo: getattr(obj, campo) for campo in self.campos}
        dados.update({k: (str(v).strip() if k != "carga_horaria" else v) for k, v in alteracoes.items() if v is not None and str(v).strip()})
        if any(not str(dados[c]).strip() for c in self.campos):
            raise ValueError("Todos os campos são obrigatórios.")
        if self.modelo is Curso:
            modalidade = str(dados["modalidade"]).upper()
            if modalidade not in ("PRESENCIAL", "EAD"):
                raise ValueError("Modalidade deve ser Presencial ou EAD.")
            dados["modalidade"] = "Presencial" if modalidade == "PRESENCIAL" else "EAD"
        if self.modelo is Disciplina:
            try:
                dados["carga_horaria"] = int(dados["carga_horaria"])
            except (ValueError, TypeError):
                raise ValueError("Carga horária deve ser um número inteiro.")
            if dados["carga_horaria"] <= 0:
                raise ValueError("Carga horária deve ser maior que zero.")
        self.validar_relacionamentos(dados)
        for campo in self.campos:
            if campo != self.identificador:
                setattr(obj, campo, dados[campo])
        self.salvar()
        return obj

    def excluir(self, identificador):
        """RF05: remove pelo identificador e sincroniza o TXT."""
        obj = self.obter(identificador)
        if obj is None:
            raise ValueError("Registro não encontrado.")
        self.registros.remove(obj)
        self.salvar()
        return obj

    def listar(self):
        return list(self.registros)

class GerenciadorCursos(GerenciadorBase):
    modelo = Curso
    arquivo_nome = "cursos.txt"
    campos = ("codigo", "nome", "modalidade")
    identificador = "codigo"

class GerenciadorProfessores(GerenciadorBase):
    modelo = Professor
    arquivo_nome = "professores.txt"
    campos = ("codigo", "nome", "cpf", "especialidade")
    identificador = "codigo"

class GerenciadorAlunos(GerenciadorBase):
    modelo = Aluno
    arquivo_nome = "alunos.txt"
    campos = ("matricula", "nome", "cpf", "email", "codigo_curso")
    identificador = "matricula"

    def __init__(self, cursos):
        self.cursos = cursos
        super().__init__()

    def validar_relacionamentos(self, dados):
        if self.cursos.obter(dados["codigo_curso"]) is None:
            raise ValueError("O código do curso não existe. Cadastre o curso antes do aluno.")

class GerenciadorDisciplinas(GerenciadorBase):
    modelo = Disciplina
    arquivo_nome = "disciplinas.txt"
    campos = ("codigo", "nome", "carga_horaria", "codigo_professor", "codigo_curso")
    identificador = "codigo"

    def __init__(self, professores, cursos):
        self.professores = professores
        self.cursos = cursos
        super().__init__()

    def validar_relacionamentos(self, dados):
        if self.professores.obter(dados["codigo_professor"]) is None:
            raise ValueError("O código do professor não existe. Cadastre o professor antes da disciplina.")
        if self.cursos.obter(dados["codigo_curso"]) is None:
            raise ValueError("O código do curso não existe. Cadastre o curso antes da disciplina.")
