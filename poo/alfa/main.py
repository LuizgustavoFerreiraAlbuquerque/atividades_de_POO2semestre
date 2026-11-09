
import tkinter as tk
from tkinter import ttk, messagebox

from gerenciador_alunos import GerenciadorAlunos
from gerenciador_cursos import GerenciadorCursos


class SistemaAcademico:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema de Gestão Acadêmica - Equipe Alfa")
        self.janela.geometry("1050x650")
        self.janela.minsize(850, 550)

        self.alunos = GerenciadorAlunos()
        self.cursos = GerenciadorCursos()

        self.configurar_estilo()

        titulo = tk.Label(
            janela,
            text="SISTEMA DE GESTÃO ACADÊMICA",
            font=("Arial", 20, "bold"),
            bg="#17365D",
            fg="white",
            pady=18
        )
        titulo.pack(fill="x")

        subtitulo = tk.Label(
            janela,
            text="EQUIPE ALFA | Gestão de Alunos e Cursos",
            font=("Arial", 11),
            pady=8
        )
        subtitulo.pack()

        self.abas = ttk.Notebook(janela)
        self.abas.pack(fill="both", expand=True, padx=15, pady=10)

        self.aba_alunos = ttk.Frame(self.abas, padding=12)
        self.aba_cursos = ttk.Frame(self.abas, padding=12)

        self.abas.add(self.aba_alunos, text="  Alunos  ")
        self.abas.add(self.aba_cursos, text="  Cursos  ")

        self.criar_aba_alunos()
        self.criar_aba_cursos()

        self.atualizar_tabelas()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Treeview",
            rowheight=27,
            font=("Arial", 10)
        )
        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )
        estilo.configure(
            "TButton",
            font=("Arial", 10),
            padding=6
        )

    def criar_campo(self, pai, texto, linha, coluna, variaveis):
        ttk.Label(pai, text=texto).grid(
            row=linha, column=coluna, sticky="w", padx=5, pady=5
        )

        campo = ttk.Entry(pai, width=25)
        campo.grid(
            row=linha, column=coluna + 1, sticky="ew", padx=5, pady=5
        )

        variaveis.append(campo)
        return campo

    def criar_aba_alunos(self):
        aba = self.aba_alunos

        ttk.Label(
            aba, text="Cadastro de Alunos",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 8))

        formulario = ttk.LabelFrame(
            aba, text="Dados do aluno", padding=10
        )
        formulario.pack(fill="x", pady=5)

        self.campos_aluno = []
        self.matricula = self.criar_campo(
            formulario, "Matrícula", 0, 0, self.campos_aluno
        )
        self.nome_aluno = self.criar_campo(
            formulario, "Nome", 0, 2, self.campos_aluno
        )
        self.cpf = self.criar_campo(
            formulario, "CPF", 1, 0, self.campos_aluno
        )
        self.email = self.criar_campo(
            formulario, "E-mail", 1, 2, self.campos_aluno
        )
        self.codigo_curso_aluno = self.criar_campo(
            formulario, "Código do curso", 2, 0, self.campos_aluno
        )

        botoes = ttk.Frame(aba)
        botoes.pack(fill="x", pady=8)

        ttk.Button(
            botoes, text="Cadastrar",
            command=self.cadastrar_aluno
        ).pack(side="left", padx=4)

        ttk.Button(
            botoes, text="Alterar selecionado",
            command=self.alterar_aluno
        ).pack(side="left", padx=4)

        ttk.Button(
            botoes, text="Excluir selecionado",
            command=self.excluir_aluno
        ).pack(side="left", padx=4)

        ttk.Button(
            botoes, text="Limpar campos",
            command=self.limpar_aluno
        ).pack(side="left", padx=4)

        busca = ttk.Frame(aba)
        busca.pack(fill="x", pady=5)

        ttk.Label(busca, text="Pesquisar por matrícula ou nome:").pack(
            side="left", padx=5
        )

        self.busca_aluno = ttk.Entry(busca, width=30)
        self.busca_aluno.pack(side="left", padx=5)

        ttk.Button(
            busca, text="Pesquisar",
            command=self.pesquisar_aluno
        ).pack(side="left", padx=3)

        ttk.Button(
            busca, text="Mostrar todos",
            command=self.atualizar_alunos
        ).pack(side="left", padx=3)

        colunas = ("matricula", "nome", "cpf", "email", "curso")
        quadro = ttk.Frame(aba)
        quadro.pack(fill="both", expand=True, pady=5)

        self.tabela_alunos = ttk.Treeview(
            quadro, columns=colunas, show="headings"
        )

        titulos = {
            "matricula": "Matrícula",
            "nome": "Nome",
            "cpf": "CPF",
            "email": "E-mail",
            "curso": "Código do curso"
        }

        larguras = {
            "matricula": 100, "nome": 180, "cpf": 130,
            "email": 200, "curso": 120
        }

        for coluna in colunas:
            self.tabela_alunos.heading(
                coluna, text=titulos[coluna]
            )
            self.tabela_alunos.column(
                coluna, width=larguras[coluna], anchor="center"
            )

        barra = ttk.Scrollbar(
            quadro, orient="vertical",
            command=self.tabela_alunos.yview
        )
        self.tabela_alunos.configure(yscrollcommand=barra.set)
        self.tabela_alunos.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.tabela_alunos.bind(
            "<<TreeviewSelect>>", self.selecionar_aluno
        )

    def criar_aba_cursos(self):
        aba = self.aba_cursos

        ttk.Label(
            aba, text="Cadastro de Cursos",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 8))

        formulario = ttk.LabelFrame(
            aba, text="Dados do curso", padding=10
        )
        formulario.pack(fill="x", pady=5)

        self.campos_curso = []
        self.codigo_curso = self.criar_campo(
            formulario, "Código", 0, 0, self.campos_curso
        )
        self.nome_curso = self.criar_campo(
            formulario, "Nome do curso", 0, 2, self.campos_curso
        )

        ttk.Label(formulario, text="Modalidade").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.modalidade = ttk.Combobox(
            formulario,
            values=("Presencial", "EAD"),
            state="readonly",
            width=22
        )
        self.modalidade.grid(
            row=1, column=1, sticky="ew", padx=5, pady=5
        )

        botoes = ttk.Frame(aba)
        botoes.pack(fill="x", pady=8)

        ttk.Button(
            botoes, text="Cadastrar",
            command=self.cadastrar_curso
        ).pack(side="left", padx=4)

        ttk.Button(
            botoes, text="Alterar selecionado",
            command=self.alterar_curso
        ).pack(side="left", padx=4)

        ttk.Button(
            botoes, text="Excluir selecionado",
            command=self.excluir_curso
        ).pack(side="left", padx=4)

        ttk.Button(
            botoes, text="Limpar campos",
            command=self.limpar_curso
        ).pack(side="left", padx=4)

        busca = ttk.Frame(aba)
        busca.pack(fill="x", pady=5)

        ttk.Label(busca, text="Pesquisar por código ou nome:").pack(
            side="left", padx=5
        )

        self.busca_curso = ttk.Entry(busca, width=30)
        self.busca_curso.pack(side="left", padx=5)

        ttk.Button(
            busca, text="Pesquisar",
            command=self.pesquisar_curso
        ).pack(side="left", padx=3)

        ttk.Button(
            busca, text="Mostrar todos",
            command=self.atualizar_cursos
        ).pack(side="left", padx=3)

        colunas = ("codigo", "nome", "modalidade")
        self.tabela_cursos = ttk.Treeview(
            aba, columns=colunas, show="headings", height=10
        )

        self.tabela_cursos.heading("codigo", text="Código")
        self.tabela_cursos.heading("nome", text="Nome do curso")
        self.tabela_cursos.heading("modalidade", text="Modalidade")

        self.tabela_cursos.column("codigo", width=150, anchor="center")
        self.tabela_cursos.column("nome", width=350)
        self.tabela_cursos.column("modalidade", width=180, anchor="center")

        self.tabela_cursos.pack(fill="both", expand=True, pady=8)
        self.tabela_cursos.bind(
            "<<TreeviewSelect>>", self.selecionar_curso
        )

    def atualizar_tabelas(self):
        self.atualizar_alunos()
        self.atualizar_cursos()

    def atualizar_alunos(self, lista=None):
        self.tabela_alunos.delete(
            *self.tabela_alunos.get_children()
        )

        for a in (self.alunos.alunos if lista is None else lista):
            self.tabela_alunos.insert(
                "", "end",
                values=(
                    a.matricula, a.nome, a.cpf,
                    a.email, a.codigo_curso
                )
            )

    def atualizar_cursos(self, lista=None):
        self.tabela_cursos.delete(
            *self.tabela_cursos.get_children()
        )

        for c in (self.cursos.cursos if lista is None else lista):
            self.tabela_cursos.insert(
                "", "end",
                values=(c.codigo, c.nome, c.modalidade)
            )

    def cadastrar_aluno(self):
        valores = [c.get().strip() for c in self.campos_aluno]

        if not all(valores):
            messagebox.showwarning(
                "Atenção", "Preencha todos os campos do aluno."
            )
            return

        matricula, nome, cpf, email, codigo = valores
        codigos = {c.codigo for c in self.cursos.cursos}

        if codigo not in codigos:
            messagebox.showerror(
                "Erro", "Cadastre primeiro o curso informado."
            )
            return

        if any(a.matricula == matricula for a in self.alunos.alunos):
            messagebox.showerror(
                "Erro", "Essa matrícula já está cadastrada."
            )
            return

        self.alunos.cadastrar(
            matricula, nome, cpf, email, codigo, codigos
        )
        self.atualizar_alunos()
        self.limpar_aluno()
        messagebox.showinfo("Sucesso", "Aluno cadastrado!")

    def selecionar_aluno(self, evento=None):
        selecionados = self.tabela_alunos.selection()
        if not selecionados:
            return

        valores = self.tabela_alunos.item(
            selecionados[0], "values"
        )

        for campo, valor in zip(self.campos_aluno, valores):
            campo.delete(0, tk.END)
            campo.insert(0, valor)

        self.matricula.config(state="disabled")

    def alterar_aluno(self):
        matricula = self.matricula.get().strip()
        aluno = next(
            (a for a in self.alunos.alunos
             if a.matricula == matricula), None
        )

        if aluno is None:
            messagebox.showwarning(
                "Atenção", "Selecione um aluno na tabela."
            )
            return

        nome = self.nome_aluno.get().strip()
        cpf = self.cpf.get().strip()
        email = self.email.get().strip()
        codigo = self.codigo_curso_aluno.get().strip()

        if not all((nome, cpf, email, codigo)):
            messagebox.showwarning(
                "Atenção", "Preencha todos os campos."
            )
            return

        if codigo not in {c.codigo for c in self.cursos.cursos}:
            messagebox.showerror("Erro", "Curso não encontrado.")
            return

        aluno.nome = nome
        aluno.cpf = cpf
        aluno.email = email
        aluno.codigo_curso = codigo
        self.alunos.salvar()
        self.atualizar_alunos()
        self.limpar_aluno()
        messagebox.showinfo("Sucesso", "Aluno alterado!")

    def excluir_aluno(self):
        selecionados = self.tabela_alunos.selection()
        if not selecionados:
            messagebox.showwarning(
                "Atenção", "Selecione um aluno na tabela."
            )
            return

        matricula = self.tabela_alunos.item(
            selecionados[0], "values"
        )[0]

        if messagebox.askyesno(
            "Confirmar", "Deseja excluir este aluno?"
        ):
            self.alunos.excluir(matricula)
            self.atualizar_alunos()
            self.limpar_aluno()

    def pesquisar_aluno(self):
        termo = self.busca_aluno.get().strip()
        if not termo:
            self.atualizar_alunos()
            return
        self.atualizar_alunos(self.alunos.pesquisar(termo))

    def limpar_aluno(self):
        self.matricula.config(state="normal")
        for campo in self.campos_aluno:
            campo.delete(0, tk.END)
        for item in self.tabela_alunos.selection():
            self.tabela_alunos.selection_remove(item)

    def cadastrar_curso(self):
        codigo = self.codigo_curso.get().strip()
        nome = self.nome_curso.get().strip()
        modalidade = self.modalidade.get().strip()

        if not codigo or not nome or not modalidade:
            messagebox.showwarning(
                "Atenção", "Preencha todos os campos do curso."
            )
            return

        if any(c.codigo == codigo for c in self.cursos.cursos):
            messagebox.showerror(
                "Erro", "Esse código já está cadastrado."
            )
            return

        self.cursos.cadastrar(codigo, nome, modalidade)
        self.atualizar_cursos()
        self.limpar_curso()
        messagebox.showinfo("Sucesso", "Curso cadastrado!")

    def selecionar_curso(self, evento=None):
        selecionados = self.tabela_cursos.selection()
        if not selecionados:
            return

        valores = self.tabela_cursos.item(
            selecionados[0], "values"
        )

        for campo, valor in zip(
            (self.codigo_curso, self.nome_curso), valores[:2]
        ):
            campo.delete(0, tk.END)
            campo.insert(0, valor)

        self.modalidade.set(valores[2].upper().replace("PRESENCIAL", "Presencial"))

        self.codigo_curso.config(state="disabled")

    def alterar_curso(self):
        codigo = self.codigo_curso.get().strip()
        curso = next(
            (c for c in self.cursos.cursos if c.codigo == codigo),
            None
        )

        if curso is None:
            messagebox.showwarning(
                "Atenção", "Selecione um curso na tabela."
            )
            return

        nome = self.nome_curso.get().strip()
        modalidade = self.modalidade.get().strip().upper()

        if not nome or modalidade not in ("PRESENCIAL", "EAD"):
            messagebox.showwarning(
                "Atenção", "Informe um nome e uma modalidade válida."
            )
            return

        curso.nome = nome
        curso.modalidade = modalidade
        self.cursos.salvar()
        self.atualizar_cursos()
        self.limpar_curso()
        messagebox.showinfo("Sucesso", "Curso alterado!")

    def excluir_curso(self):
        selecionados = self.tabela_cursos.selection()
        if not selecionados:
            messagebox.showwarning(
                "Atenção", "Selecione um curso na tabela."
            )
            return

        codigo = self.tabela_cursos.item(
            selecionados[0], "values"
        )[0]

        if any(a.codigo_curso == codigo for a in self.alunos.alunos):
            messagebox.showerror(
                "Erro", "Não é possível excluir: existem alunos vinculados."
            )
            return

        if messagebox.askyesno(
            "Confirmar", "Deseja excluir este curso?"
        ):
            self.cursos.excluir(codigo)
            self.atualizar_cursos()
            self.limpar_curso()

    def pesquisar_curso(self):
        termo = self.busca_curso.get().strip()
        if not termo:
            self.atualizar_cursos()
            return
        self.atualizar_cursos(self.cursos.pesquisar(termo))

    def limpar_curso(self):
        self.codigo_curso.config(state="normal")
        self.codigo_curso.delete(0, tk.END)
        self.nome_curso.delete(0, tk.END)
        self.modalidade.set("")
        for item in self.tabela_cursos.selection():
            self.tabela_cursos.selection_remove(item)


if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaAcademico(janela)
    janela.mainloop()