"""Sistema de Gestão Acadêmica Integrado — execute com: python main.py"""
from gerenciadores.gerenciador_avaliacoes import GerenciadorAvaliacoes, CAMPOS
from gerenciadores.gerenciadores import (
    GerenciadorAlunos, GerenciadorCursos,
    GerenciadorProfessores, GerenciadorDisciplinas,
)


def ler(rotulo, atual=None):
    if atual is None:
        return input(f"{rotulo}: ").strip()
    valor = input(f"{rotulo} [{atual}]: ").strip()
    return valor if valor else str(atual)


def mostrar(registros):
    if not registros:
        print("Nenhum registro encontrado.")
        return
    for obj in registros:
        print(" | ".join(f"{campo}={valor}" for campo, valor in vars(obj).items()))


def operacoes(nome, gerenciador, campos, rotulo_id):
    while True:
        print(f"\n--- {nome.upper()} ---")
        print("1. Cadastrar\n2. Listar\n3. Pesquisar por código/matrícula ou nome\n4. Alterar\n5. Excluir\n0. Voltar")
        opcao = input("Escolha: ").strip()
        try:
            if opcao == "1":
                dados = {campo: ler(rotulo) for campo, rotulo in campos}
                gerenciador.cadastrar(**dados)
                print("Cadastro realizado e salvo com sucesso.")
            elif opcao == "2":
                mostrar(gerenciador.listar())
            elif opcao == "3":
                termo = ler("Digite o identificador ou nome")
                mostrar(gerenciador.pesquisar(termo))
            elif opcao == "4":
                identificador = ler(f"{rotulo_id} do registro a alterar")
                obj = gerenciador.obter(identificador)
                if obj is None:
                    print("Registro não encontrado.")
                    continue
                alteracoes = {campo: ler(rotulo, getattr(obj, campo)) for campo, rotulo in campos if campo != gerenciador.identificador}
                gerenciador.alterar(identificador, **alteracoes)
                print("Alteração realizada e salva com sucesso.")
            elif opcao == "5":
                identificador = ler(f"{rotulo_id} do registro a excluir")
                if input(f"Confirma excluir {identificador}? (s/n): ").strip().lower() == "s":
                    gerenciador.excluir(identificador)
                    print("Registro excluído e arquivo atualizado.")
            elif opcao == "0":
                return
            else:
                print("Opção inválida.")
        except (ValueError, OSError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")


def relatorio(alunos, cursos, disciplinas, professores):
    print("\n--- RELATÓRIO INTEGRADO ---")
    total = 0
    for aluno in alunos.listar():
        curso = cursos.obter(aluno.codigo_curso)
        if curso is None:
            print(f"Aluno {aluno.nome}: curso {aluno.codigo_curso} não encontrado.")
            continue
        vinculadas = [d for d in disciplinas.listar() if d.codigo_curso == curso.codigo]
        if not vinculadas:
            print(f"Aluno {aluno.nome} está matriculado no curso {curso.nome}, mas não há disciplinas cadastradas para esse curso.")
            continue
        for disciplina in vinculadas:
            professor = professores.obter(disciplina.codigo_professor)
            if professor is None:
                print(f"Disciplina {disciplina.nome}: professor {disciplina.codigo_professor} não encontrado.")
                continue
            print(f"O Aluno {aluno.nome} está matriculado no curso {curso.nome}, assistindo a disciplina {disciplina.nome} com o professor {professor.nome}")
            total += 1
    if total == 0:
        print("Nenhum relacionamento completo encontrado. Cadastre e vincule as entidades.")


def menu_avaliacoes(gerenciador):
    while True:
        print("\n--- AVALIAÇÕES E NOTAS ---")
        print("1. Cadastrar avaliação\n2. Listar avaliações\n3. Alterar notas e pesos\n4. Excluir avaliação\n5. Relatório de rendimento\n0. Voltar")
        opcao = input("Escolha: ").strip()
        try:
            if opcao in ("1", "3"):
                matricula = ler("Matrícula do aluno")
                codigo = ler("Código da disciplina")
                valores = []
                anterior = next((a for a in gerenciador.listar() if a.matricula == matricula and a.codigo_disciplina == codigo), None) if opcao == "3" else None
                if opcao == "3" and anterior is None:
                    print("Avaliação não encontrada.")
                    continue
                for campo in CAMPOS:
                    valores.append(ler(campo.capitalize(), getattr(anterior, campo) if anterior else None))
                a = gerenciador.cadastrar(matricula, codigo, *valores) if opcao == "1" else gerenciador.alterar(matricula, codigo, *valores)
                print(f"Salvo! Média: {a.media:.2f} | {a.status}")
            elif opcao == "2":
                registros = gerenciador.listar()
                if not registros:
                    print("Nenhuma avaliação cadastrada.")
                for a in registros:
                    print(f"{a.matricula} | {a.codigo_disciplina} | Média: {a.media:.2f} | {a.status}")
            elif opcao == "4":
                matricula = ler("Matrícula")
                codigo = ler("Código da disciplina")
                if input("Confirma exclusão? (s/n): ").strip().lower() == "s":
                    gerenciador.excluir(matricula, codigo)
                    print("Avaliação excluída.")
            elif opcao == "5":
                gerenciador.relatorio()
            elif opcao == "0":
                return
            else:
                print("Opção inválida.")
        except (ValueError, OSError) as erro:
            print(f"Erro: {erro}")


def main():
    # RF11: os gerenciadores carregam automaticamente os TXT ao iniciar.
    cursos = GerenciadorCursos()
    professores = GerenciadorProfessores()
    alunos = GerenciadorAlunos(cursos)
    disciplinas = GerenciadorDisciplinas(professores, cursos)
    avaliacoes = GerenciadorAvaliacoes(alunos, disciplinas)
    while True:
        print("\n==========================================")
        print(" SISTEMA DE GESTÃO ACADÊMICA INTEGRADO")
        print("==========================================")
        print("1. Alunos\n2. Cursos\n3. Professores\n4. Disciplinas\n5. Relatório integrado\n6. Avaliações e Notas\n0. Encerrar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            operacoes("Alunos", alunos, [("matricula", "Matrícula"), ("nome", "Nome"), ("cpf", "CPF"), ("email", "E-mail"), ("codigo_curso", "Código do curso")], "Matrícula")
        elif opcao == "2":
            operacoes("Cursos", cursos, [("codigo", "Código do curso"), ("nome", "Nome"), ("modalidade", "Modalidade (Presencial/EAD)")], "Código")
        elif opcao == "3":
            operacoes("Professores", professores, [("codigo", "Código do professor"), ("nome", "Nome"), ("cpf", "CPF"), ("especialidade", "Especialidade")], "Código")
        elif opcao == "4":
            operacoes("Disciplinas", disciplinas, [("codigo", "Código da disciplina"), ("nome", "Nome"), ("carga_horaria", "Carga horária"), ("codigo_professor", "Código do professor"), ("codigo_curso", "Código do curso")], "Código")
        elif opcao == "5":
            relatorio(alunos, cursos, disciplinas, professores)
        elif opcao == "6":
            menu_avaliacoes(avaliacoes)
        elif opcao == "0":
            print("Sistema encerrado. Todos os dados cadastrados já foram salvos.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
