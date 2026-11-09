import os
from pathlib import Path
from aluno import Aluno


class GerenciadorAlunos:
    def __init__(self, arquivo=None):
        self.arquivo = str(Path(arquivo) if arquivo else Path(__file__).resolve().parent.parent / "dados" / "alunos.txt")
        self.alunos = []
        self.carregar()

    def carregar(self):
        self.alunos = []

        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    dados = linha.rstrip("\n").split(";")

                    if len(dados) == 5:
                        matricula, nome, cpf, email, codigo_curso = dados
                        self.alunos.append(
                            Aluno(matricula, nome, cpf, email, codigo_curso)
                        )
        except FileNotFoundError:
            pass

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            for aluno in self.alunos:
                dados = [
                    aluno.matricula,
                    aluno.nome,
                    aluno.cpf,
                    aluno.email,
                    aluno.codigo_curso
                ]
                arquivo.write(";".join(dados) + "\n")

    def pesquisar(self, termo):
        termo = termo.strip().casefold()

        return [
            aluno for aluno in self.alunos
            if termo == aluno.matricula.casefold()
            or termo in aluno.nome.casefold()
        ]

    def cadastrar(self, matricula, nome, cpf, email, codigo_curso,
                  codigos_cursos):
        if not all(v.strip() for v in (
            matricula, nome, cpf, email, codigo_curso
        )):
            print("Todos os campos são obrigatórios.")
            return

        if any(a.matricula == matricula for a in self.alunos):
            print("Já existe um aluno com essa matrícula.")
            return

        if codigo_curso not in codigos_cursos:
            print("Curso não encontrado. Cadastre o curso primeiro.")
            return

        aluno = Aluno(
            matricula.strip(),
            nome.strip(),
            cpf.strip(),
            email.strip(),
            codigo_curso.strip()
        )

        self.alunos.append(aluno)
        self.salvar()
        print("Aluno cadastrado com sucesso!")

    def listar(self):
        if not self.alunos:
            print("Nenhum aluno cadastrado.")
            return

        for aluno in self.alunos:
            print(aluno)

    def alterar(self, matricula, codigos_cursos):
        resultados = [
            a for a in self.alunos if a.matricula == matricula
        ]

        if not resultados:
            print("Aluno não encontrado.")
            return

        aluno = resultados[0]

        nome = input("Novo nome (Enter mantém): ").strip()
        cpf = input("Novo CPF (Enter mantém): ").strip()
        email = input("Novo e-mail (Enter mantém): ").strip()
        codigo = input("Novo código do curso (Enter mantém): ").strip()

        if codigo and codigo not in codigos_cursos:
            print("Curso não encontrado. Alteração cancelada.")
            return

        if nome:
            aluno.nome = nome
        if cpf:
            aluno.cpf = cpf
        if email:
            aluno.email = email
        if codigo:
            aluno.codigo_curso = codigo

        self.salvar()
        print("Aluno alterado com sucesso!")

    def excluir(self, matricula):
        resultados = [
            a for a in self.alunos if a.matricula == matricula
        ]

        if not resultados:
            print("Aluno não encontrado.")
            return

        self.alunos.remove(resultados[0])
        self.salvar()
        print("Aluno excluído com sucesso!")

class GerenciadorAluno:
    def __init__(self, caminho_alunos="dados/alunos.txt", caminho_cursos="dados/cursos.txt"):
        self.caminho_alunos = caminho_alunos
        self.caminho_cursos = caminho_cursos

    # -------------------------------------------------------------
    # 📍 AQUI ENTRA A VALIDAÇÃO: Verificar se o Curso Existe
    # -------------------------------------------------------------
    def validar_curso_existe(self, cod_curso: str) -> bool:
        if not os.path.exists(self.caminho_cursos):
            return False
        with open(self.caminho_cursos, "r", encoding="utf-8") as file:
            for linha in file:
                dados = linha.strip().split(";")
                if dados and dados[0] == str(cod_curso):
                    return True
        return False

    # -------------------------------------------------------------
    # 📍 AQUI ENTRA A VALIDAÇÃO: Verificar se a Matrícula é Única
    # -------------------------------------------------------------
    def validar_matricula_unica(self, matricula: str) -> bool:
        if not os.path.exists(self.caminho_alunos):
            return True  # Se o arquivo não existe, a matrícula é única
        with open(self.caminho_alunos, "r", encoding="utf-8") as file:
            for linha in file:
                dados = linha.strip().split(";")
                if dados and dados[0] == str(matricula):
                    return False  # Matrícula já existe!
        return True

    # -------------------------------------------------------------
    # 📍 AQUI ENTRA O ENCAIXE NO MÉTODO DE CADASTRO
    # -------------------------------------------------------------
    def cadastrar(self, aluno: Aluno):
        # Validação 1: Testar duplicidade
        if not self.validar_matricula_unica(aluno.matricula):
            raise ValueError(f"A matrícula {aluno.matricula} já está cadastrada no sistema!")

        # Validação 2: Testar se o curso vinculado realmente existe
        if not self.validar_curso_existe(aluno.cod_curso):
            raise ValueError(f"O Código de Curso '{aluno.cod_curso}' não existe em cursos.txt!")

        # Gravação no arquivo se passar em todas as validações
        with open(self.caminho_alunos, "a", encoding="utf-8") as file:
            file.write(str(aluno) + "\n")
        return True

    import re
import tkinter as tk
from tkinter import ttk, messagebox
from aluno import Aluno

class AbaAluno(ttk.Frame):
    def __init__(self, parent, gerenciador_aluno):
        super().__init__(parent)
        self.gerenciador = gerenciador_aluno
        self.criar_componentes_tela()

    def criar_componentes_tela(self):
        # Exemplo simples de campos de texto (Entry) na tela
        self.ent_matricula = ttk.Entry(self)
        self.ent_nome = ttk.Entry(self)
        self.ent_cpf = ttk.Entry(self)
        self.ent_email = ttk.Entry(self)
        self.ent_curso = ttk.Entry(self)
        
        btn_salvar = ttk.Button(self, text="Salvar Aluno", command=self.acao_salvar)
        btn_salvar.pack()

    # -------------------------------------------------------------
    # 📍 AQUI ENTRA O ENCAIXE DAS VALIDAÇÕES DA INTERFACE GRÁFICA
    # -------------------------------------------------------------
    def acao_salvar(self):
        # 1. Pega os valores das caixas da tela
        matricula = self.ent_matricula.get().strip()
        nome = self.ent_nome.get().strip()
        cpf = self.ent_cpf.get().strip()
        email = self.ent_email.get().strip()
        cod_curso = self.ent_curso.get().strip()

        # 📍 Validação A: Campos Obrigatórios Vazios
        if not matricula or not nome or not cpf or not email or not cod_curso:
            messagebox.showwarning("Atenção", "Preencha todos os campos do formulário!")
            return

        # 📍 Validação B: Matrícula e CPF devem ter apenas dígitos
        if not matricula.isdigit():
            messagebox.showwarning("Atenção", "A Matrícula deve conter apenas números!")
            return

        cpf_somente_numeros = re.sub(r"\D", "", cpf)
        if len(cpf_somente_numeros) != 11:
            messagebox.showwarning("Atenção", "O CPF deve ter exatamente 11 dígitos numéricos!")
            return

        # 📍 Validação C: Formato do E-mail (Presença de @ e .)
        padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(padrao_email, email):
            messagebox.showwarning("Atenção", "Digite um e-mail válido (exemplo: aluno@email.com)!")
            return

        # -------------------------------------------------------------
        # 📍 ENCAIXE COM O GERENCIADOR (Manda salvar e trata os erros de arquivo)
        # -------------------------------------------------------------
        try:
            novo_aluno = Aluno(matricula, nome, cpf, email, cod_curso)
            self.gerenciador.cadastrar(novo_aluno)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            
        except ValueError as erro:
            # Pega os erros que vieram do gerenciador (ex: curso não existe, matrícula duplicada)
            messagebox.showerror("Erro de Regra de Negócio", str(erro))