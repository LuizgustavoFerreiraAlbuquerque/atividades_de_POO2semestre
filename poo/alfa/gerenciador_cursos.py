from pathlib import Path
from curso import Curso


class GerenciadorCursos:
    def __init__(self, arquivo=None):
        self.arquivo = str(Path(arquivo) if arquivo else Path(__file__).resolve().parent.parent / "dados" / "cursos.txt")
        self.cursos = []
        self.carregar()

    def carregar(self):
        self.cursos = []

        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    dados = linha.rstrip("\n").split(";")

                    if len(dados) == 3:
                        codigo, nome, modalidade = dados
                        self.cursos.append(
                            Curso(codigo, nome, modalidade)
                        )
        except FileNotFoundError:
            pass

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            for curso in self.cursos:
                dados = [
                    curso.codigo,
                    curso.nome,
                    curso.modalidade
                ]
                arquivo.write(";".join(dados) + "\n")

    def pesquisar(self, termo):
        termo = termo.strip().casefold()

        return [
            curso for curso in self.cursos
            if termo == curso.codigo.casefold()
            or termo in curso.nome.casefold()
        ]

    def cadastrar(self, codigo, nome, modalidade):
        if not codigo.strip() or not nome.strip():
            print("Código e nome são obrigatórios.")
            return

        if any(c.codigo == codigo for c in self.cursos):
            print("Já existe um curso com esse código.")
            return

        modalidade = modalidade.strip().upper()

        if modalidade not in ("PRESENCIAL", "EAD"):
            print("Modalidade inválida. Use Presencial ou EAD.")
            return

        curso = Curso(codigo.strip(), nome.strip(), modalidade)
        self.cursos.append(curso)
        self.salvar()
        print("Curso cadastrado com sucesso!")

    def listar(self):
        if not self.cursos:
            print("Nenhum curso cadastrado.")
            return

        for curso in self.cursos:
            print(curso)

    def alterar(self, codigo):
        resultados = [
            c for c in self.cursos if c.codigo == codigo
        ]

        if not resultados:
            print("Curso não encontrado.")
            return

        curso = resultados[0]
        novo_nome = input("Novo nome (Enter mantém): ").strip()
        nova_modalidade = input(
            "Nova modalidade (Enter mantém): "
        ).strip().upper()

        if novo_nome:
            curso.nome = novo_nome

        if nova_modalidade:
            if nova_modalidade not in ("PRESENCIAL", "EAD"):
                print("Modalidade inválida. Alteração cancelada.")
                return
            curso.modalidade = nova_modalidade

        self.salvar()
        print("Curso alterado com sucesso!")

    def excluir(self, codigo):
        resultados = [
            c for c in self.cursos if c.codigo == codigo
        ]

        if not resultados:
            print("Curso não encontrado.")
            return

        self.cursos.remove(resultados[0])
        self.salvar()
        print("Curso excluído com sucesso!")