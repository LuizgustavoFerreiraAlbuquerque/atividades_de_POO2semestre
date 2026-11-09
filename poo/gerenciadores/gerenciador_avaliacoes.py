"""RF19-RF24: notas persistidas, validação e cálculo em tempo de leitura."""
from pathlib import Path
import math
from modelos.avaliacao import Avaliacao

ARQUIVO = Path(__file__).resolve().parent.parent / "dados" / "notas.txt"
CAMPOS = ("nota1", "peso1", "nota2", "peso2", "nota3", "peso3")

class GerenciadorAvaliacoes:
    def __init__(self, alunos, disciplinas):
        self.alunos = alunos
        self.disciplinas = disciplinas
        ARQUIVO.parent.mkdir(exist_ok=True)
        ARQUIVO.touch(exist_ok=True)

    def validar(self, matricula, codigo_disciplina, valores):
        self.alunos.carregar()
        self.disciplinas.carregar()
        aluno = self.alunos.obter(matricula)
        disciplina = self.disciplinas.obter(codigo_disciplina)
        if aluno is None:
            raise ValueError("Matrícula não encontrada em alunos.txt.")
        if disciplina is None:
            raise ValueError("Disciplina não encontrada em disciplinas.txt.")
        if aluno.codigo_curso != disciplina.codigo_curso:
            raise ValueError("A disciplina não pertence ao curso do aluno.")
        numeros = []
        for campo, valor in zip(CAMPOS, valores):
            try:
                numero = float(str(valor).replace(",", "."))
            except (ValueError, TypeError):
                raise ValueError(f"{campo} deve ser numérico.")
            if not math.isfinite(numero):
                raise ValueError(f"{campo} deve ser finito.")
            if campo.startswith("nota") and not 0 <= numero <= 10:
                raise ValueError(f"{campo} deve estar entre 0 e 10.")
            if campo.startswith("peso") and numero < 0:
                raise ValueError(f"{campo} não pode ser negativo.")
            numeros.append(numero)
        if sum(numeros[1::2]) <= 0:
            raise ValueError("A soma dos pesos deve ser maior que zero.")
        return Avaliacao(matricula, codigo_disciplina, *numeros)

    def listar(self):
        """Reabre o TXT a cada consulta, refletindo alterações externas."""
        registros = []
        with ARQUIVO.open(encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, 1):
                if not linha.strip():
                    continue
                partes = linha.strip().split(";")
                if len(partes) != 8:
                    print(f"Aviso: notas.txt linha {numero}: são necessários 8 campos.")
                    continue
                try:
                    registros.append(self.validar(partes[0], partes[1], partes[2:]))
                except ValueError as erro:
                    print(f"Aviso: notas.txt linha {numero}: {erro}")
        return registros

    def salvar(self, registros):
        with ARQUIVO.open("w", encoding="utf-8") as arquivo:
            for a in registros:
                arquivo.write(";".join([a.matricula, a.codigo_disciplina] + [str(getattr(a, campo)) for campo in CAMPOS]) + "\n")

    def cadastrar(self, matricula, codigo_disciplina, *valores):
        registros = self.listar()
        if any(a.matricula == matricula and a.codigo_disciplina == codigo_disciplina for a in registros):
            raise ValueError("Já existe avaliação deste aluno nesta disciplina.")
        avaliacao = self.validar(matricula, codigo_disciplina, valores)
        registros.append(avaliacao)
        self.salvar(registros)
        return avaliacao

    def alterar(self, matricula, codigo_disciplina, *valores):
        registros = self.listar()
        for indice, a in enumerate(registros):
            if a.matricula == matricula and a.codigo_disciplina == codigo_disciplina:
                nova = self.validar(matricula, codigo_disciplina, valores)
                registros[indice] = nova
                self.salvar(registros)
                return nova
        raise ValueError("Avaliação não encontrada.")

    def excluir(self, matricula, codigo_disciplina):
        registros = self.listar()
        novos = [a for a in registros if (a.matricula, a.codigo_disciplina) != (matricula, codigo_disciplina)]
        if len(novos) == len(registros):
            raise ValueError("Avaliação não encontrada.")
        self.salvar(novos)

    def relatorio(self):
        self.alunos.carregar()
        self.disciplinas.carregar()
        registros = self.listar()
        if not registros:
            print("Nenhuma avaliação cadastrada.")
        for a in registros:
            aluno = self.alunos.obter(a.matricula)
            disciplina = self.disciplinas.obter(a.codigo_disciplina)
            print("\n" + "=" * 48)
            print(f"Aluno: {aluno.nome} | Matrícula: {a.matricula}")
            print(f"Disciplina: {disciplina.nome} ({a.codigo_disciplina})")
            for i in range(1, 4):
                print(f"Nota {i}: {getattr(a, 'nota'+str(i)):.2f} | Peso {i}: {getattr(a, 'peso'+str(i)):g}")
            print(f"Média final: {a.media:.2f} | Status: {a.status}")
