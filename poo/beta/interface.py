import tkinter as tk
from tkinter import ttk, messagebox

from gerenciador_professores import GerenciadorProfessores
from gerenciador_disciplinas import GerenciadorDisciplinas
from gerenciador_cursos import GerenciadorCursos


class AplicacaoBeta:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema de Gestão Acadêmica - Equipe BETA")
        self.janela.geometry("1000x650")
        self.janela.minsize(850, 550)

        self.professores = GerenciadorProfessores()
        self.disciplinas = GerenciadorDisciplinas()
        self.cursos = GerenciadorCursos()

        titulo = ttk.Label(
            janela, text="Sistema de Gestão Acadêmica — Equipe BETA",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=(12, 6))

        self.abas = ttk.Notebook(janela)
        self.abas.pack(fill="both", expand=True, padx=12, pady=12)

        self.aba_professores = ttk.Frame(self.abas, padding=10)
        self.aba_disciplinas = ttk.Frame(self.abas, padding=10)
        self.abas.add(self.aba_professores, text="Professores")
        self.abas.add(self.aba_disciplinas, text="Disciplinas")

        self.criar_aba_professores()
        self.criar_aba_disciplinas()
        self.atualizar_professores()
        self.atualizar_disciplinas()

    def campo(self, pai, rotulo, linha, coluna, largura=25):
        ttk.Label(pai, text=rotulo).grid(row=linha, column=coluna, sticky="w", padx=5, pady=4)
        entrada = ttk.Entry(pai, width=largura)
        entrada.grid(row=linha, column=coluna + 1, sticky="ew", padx=5, pady=4)
        return entrada

    def criar_aba_professores(self):
        form = ttk.LabelFrame(self.aba_professores, text="Dados do professor", padding=8)
        form.pack(fill="x", pady=(0, 10))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        self.p_codigo = self.campo(form, "Código:", 0, 0)
        self.p_nome = self.campo(form, "Nome:", 0, 2)
        self.p_cpf = self.campo(form, "CPF:", 1, 0)
        self.p_especialidade = self.campo(form, "Especialidade:", 1, 2)

        botoes = ttk.Frame(form)
        botoes.grid(row=2, column=0, columnspan=4, pady=8)
        ttk.Button(botoes, text="Cadastrar", command=self.cadastrar_professor).pack(side="left", padx=4)
        ttk.Button(botoes, text="Alterar selecionado", command=self.alterar_professor).pack(side="left", padx=4)
        ttk.Button(botoes, text="Excluir selecionado", command=self.excluir_professor).pack(side="left", padx=4)
        ttk.Button(botoes, text="Limpar", command=self.limpar_professor).pack(side="left", padx=4)

        pesquisa = ttk.Frame(self.aba_professores)
        pesquisa.pack(fill="x", pady=(0, 6))
        ttk.Label(pesquisa, text="Pesquisar por código ou nome:").pack(side="left", padx=5)
        self.p_busca = ttk.Entry(pesquisa, width=30)
        self.p_busca.pack(side="left", padx=5)
        ttk.Button(pesquisa, text="Pesquisar", command=self.pesquisar_professor).pack(side="left", padx=3)
        ttk.Button(pesquisa, text="Mostrar todos", command=self.atualizar_professores).pack(side="left", padx=3)

        colunas = ("codigo", "nome", "cpf", "especialidade")
        self.tabela_p = ttk.Treeview(self.aba_professores, columns=colunas, show="headings", height=12)
        for coluna, texto, largura in [
            ("codigo", "Código", 100), ("nome", "Nome", 240),
            ("cpf", "CPF", 160), ("especialidade", "Especialidade", 220)
        ]:
            self.tabela_p.heading(coluna, text=texto)
            self.tabela_p.column(coluna, width=largura, anchor="w")
        self.tabela_p.pack(fill="both", expand=True)
        self.tabela_p.bind("<<TreeviewSelect>>", self.selecionar_professor)

    def criar_aba_disciplinas(self):
        form = ttk.LabelFrame(self.aba_disciplinas, text="Dados da disciplina", padding=8)
        form.pack(fill="x", pady=(0, 10))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        self.d_codigo = self.campo(form, "Código:", 0, 0)
        self.d_nome = self.campo(form, "Nome:", 0, 2)
        self.d_carga = self.campo(form, "Carga horária (h):", 1, 0)
        self.d_professor = self.campo(form, "Código do professor:", 1, 2)
        self.d_curso = self.campo(form, "Código do curso (ALFA):", 2, 0)

        botoes = ttk.Frame(form)
        botoes.grid(row=3, column=0, columnspan=4, pady=8)
        ttk.Button(botoes, text="Cadastrar", command=self.cadastrar_disciplina).pack(side="left", padx=4)
        ttk.Button(botoes, text="Alterar selecionada", command=self.alterar_disciplina).pack(side="left", padx=4)
        ttk.Button(botoes, text="Excluir selecionada", command=self.excluir_disciplina).pack(side="left", padx=4)
        ttk.Button(botoes, text="Limpar", command=self.limpar_disciplina).pack(side="left", padx=4)

        pesquisa = ttk.Frame(self.aba_disciplinas)
        pesquisa.pack(fill="x", pady=(0, 6))
        ttk.Label(pesquisa, text="Pesquisar por código ou nome:").pack(side="left", padx=5)
        self.d_busca = ttk.Entry(pesquisa, width=30)
        self.d_busca.pack(side="left", padx=5)
        ttk.Button(pesquisa, text="Pesquisar", command=self.pesquisar_disciplina).pack(side="left", padx=3)
        ttk.Button(pesquisa, text="Mostrar todas", command=self.atualizar_disciplinas).pack(side="left", padx=3)

        colunas = ("codigo", "nome", "carga", "professor", "curso")
        self.tabela_d = ttk.Treeview(self.aba_disciplinas, columns=colunas, show="headings", height=12)
        for coluna, texto, largura in [
            ("codigo", "Código", 85), ("nome", "Disciplina", 200),
            ("carga", "Carga horária", 110), ("professor", "Cód. professor", 120),
            ("curso", "Cód. curso", 100)
        ]:
            self.tabela_d.heading(coluna, text=texto)
            self.tabela_d.column(coluna, width=largura, anchor="w")
        self.tabela_d.pack(fill="both", expand=True)
        self.tabela_d.bind("<<TreeviewSelect>>", self.selecionar_disciplina)

    @staticmethod
    def valores(entradas):
        return [entrada.get().strip() for entrada in entradas]

    @staticmethod
    def preencher(entradas, valores):
        for entrada, valor in zip(entradas, valores):
            entrada.delete(0, tk.END)
            entrada.insert(0, str(valor))

    def limpar_professor(self):
        self.preencher([self.p_codigo, self.p_nome, self.p_cpf, self.p_especialidade], ["", "", "", ""])
        self.tabela_p.selection_remove(self.tabela_p.selection())

    def limpar_disciplina(self):
        self.preencher(
            [self.d_codigo, self.d_nome, self.d_carga, self.d_professor, self.d_curso],
            ["", "", "", "", ""]
        )
        self.tabela_d.selection_remove(self.tabela_d.selection())

    def cadastrar_professor(self):
        try:
            self.professores.cadastrar(*self.valores(
                [self.p_codigo, self.p_nome, self.p_cpf, self.p_especialidade]
            ))
            self.atualizar_professores()
            self.limpar_professor()
            messagebox.showinfo("Sucesso", "Professor cadastrado.")
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro", str(erro))

    def alterar_professor(self):
        try:
            codigo, nome, cpf, especialidade = self.valores(
                [self.p_codigo, self.p_nome, self.p_cpf, self.p_especialidade]
            )
            self.professores.alterar(codigo, nome, cpf, especialidade)
            self.atualizar_professores()
            messagebox.showinfo("Sucesso", "Professor alterado.")
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir_professor(self):
        codigo = self.p_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atenção", "Selecione um professor ou informe o código.")
            return
        if not messagebox.askyesno("Confirmar", f"Excluir o professor {codigo}?"):
            return
        try:
            self.professores.excluir(codigo)
            self.atualizar_professores()
            self.limpar_professor()
            messagebox.showinfo("Sucesso", "Professor excluído.")
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro", str(erro))

    def pesquisar_professor(self):
        resultados = self.professores.pesquisar(self.p_busca.get())
        self.mostrar_professores(resultados)

    def atualizar_professores(self):
        self.mostrar_professores(self.professores.professores)

    def mostrar_professores(self, lista):
        for item in self.tabela_p.get_children():
            self.tabela_p.delete(item)
        for p in lista:
            self.tabela_p.insert("", "end", values=(p.codigo, p.nome, p.cpf, p.especialidade))

    def selecionar_professor(self, _evento=None):
        selecao = self.tabela_p.selection()
        if not selecao:
            return
        valores = self.tabela_p.item(selecao[0], "values")
        self.preencher([self.p_codigo, self.p_nome, self.p_cpf, self.p_especialidade], valores)

    def cadastrar_disciplina(self):
        try:
            self.disciplinas.cadastrar(
                *self.valores([self.d_codigo, self.d_nome, self.d_carga, self.d_professor, self.d_curso]),
                gerenciador_professores=self.professores,
                gerenciador_cursos=self.cursos
            )
            self.atualizar_disciplinas()
            self.limpar_disciplina()
            messagebox.showinfo("Sucesso", "Disciplina cadastrada.")
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro", str(erro))

    def alterar_disciplina(self):
        try:
            codigo, nome, carga, codigo_professor, codigo_curso = self.valores(
                [self.d_codigo, self.d_nome, self.d_carga, self.d_professor, self.d_curso]
            )
            self.disciplinas.alterar(
                codigo, nome, carga, codigo_professor, codigo_curso,
                gerenciador_professores=self.professores,
                gerenciador_cursos=self.cursos
            )
            self.atualizar_disciplinas()
            messagebox.showinfo("Sucesso", "Disciplina alterada.")
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir_disciplina(self):
        codigo = self.d_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atenção", "Selecione uma disciplina ou informe o código.")
            return
        if not messagebox.askyesno("Confirmar", f"Excluir a disciplina {codigo}?"):
            return
        try:
            self.disciplinas.excluir(codigo)
            self.atualizar_disciplinas()
            self.limpar_disciplina()
            messagebox.showinfo("Sucesso", "Disciplina excluída.")
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro", str(erro))

    def pesquisar_disciplina(self):
        resultados = self.disciplinas.pesquisar(self.d_busca.get())
        self.mostrar_disciplinas(resultados)

    def atualizar_disciplinas(self):
        self.mostrar_disciplinas(self.disciplinas.disciplinas)

    def mostrar_disciplinas(self, lista):
        for item in self.tabela_d.get_children():
            self.tabela_d.delete(item)
        for d in lista:
            self.tabela_d.insert(
                "", "end",
                values=(d.codigo, d.nome, d.carga_horaria, d.codigo_professor, d.codigo_curso)
            )

    def selecionar_disciplina(self, _evento=None):
        selecao = self.tabela_d.selection()
        if not selecao:
            return
        valores = self.tabela_d.item(selecao[0], "values")
        self.preencher(
            [self.d_codigo, self.d_nome, self.d_carga, self.d_professor, self.d_curso],
            valores
        )
