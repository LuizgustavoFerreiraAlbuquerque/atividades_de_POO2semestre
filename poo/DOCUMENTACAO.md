/https://github.com/LuizgustavoFerreiraAlbuquerque/poo_alfa/tree/main/poo/
# Documentação dos Requisitos Funcionais — Sistema de Gestão Acadêmica Integrado


## Organização
- `main.py`: ponto de entrada único e menu de navegação por console.
- `modelos/entidades.py`: classes de dados `Aluno`, `Curso`, `Professor` e `Disciplina`.
- `gerenciadores/gerenciadores.py`: CRUD, validações, carregamento e gravação dos arquivos.
- `dados/alunos.txt`, `cursos.txt`, `professores.txt` e `disciplinas.txt`: persistência separada por entidade.
- `alfa/` e `beta/`: interfaces e códigos originais das equipes, preservados como referência.

## Requisitos funcionais
| RF | Implementação |
|---|---|
| RF01 | `GerenciadorBase.cadastrar()` cria novo objeto e grava no TXT. |
| RF02 | `listar()` retorna objetos carregados; o menu os exibe formatados. |
| RF03 | `pesquisar()` procura identificador exato ou parte do nome. |
| RF04 | `alterar()` atualiza atributos e salva o arquivo; identificador é preservado. |
| RF05 | `excluir()` remove pelo identificador e atualiza o TXT. |
| RF06 | `Aluno`: matrícula, nome, CPF, e-mail e código do curso. |
| RF07 | `Curso`: código, nome e modalidade Presencial ou EAD. |
| RF08 | `Professor`: código, nome, CPF e especialidade. |
| RF09 | `Disciplina`: código, nome, carga horária, código do professor e código do curso. |
| RF10 | Cada entidade usa seu próprio TXT e `;` como separador. |
| RF11 | Cada gerenciador executa `carregar()` na inicialização. |
| RF12 | Cadastro, alteração e exclusão chamam `salvar()` automaticamente. |
| RF13 | O gerenciador de alunos valida se o código do curso existe. |
| RF14 | O gerenciador de disciplinas valida professor e curso existentes. |
| RF15 | Opção 5 gera a frase com aluno, curso, disciplina e professor. |
| RF16 | `main.py` centraliza a execução de todas as entidades. |
| RF17 | Menus de console para as quatro entidades e relatório. |
| RF18 | Opção 0 encerra o programa de forma controlada. |

## Como executar
1. Instale Python 3.10 ou superior.
2. Abra a pasta `poo` no VS Code.
3. No terminal, execute `python main.py` (no Windows, também pode ser `py main.py`).
4. Cadastre primeiro os cursos e professores; depois alunos e disciplinas, pois estes dependem dos códigos já cadastrados.

## Como testar o relacionamento
1. Cadastre um curso, por exemplo código `C01`, nome `Informática`, modalidade `Presencial`.
2. Cadastre um professor, por exemplo código `P01`, nome `Ana`, CPF `123`, especialidade `Programação`.
3. Cadastre um aluno com código do curso `C01`.
4. Cadastre uma disciplina com código do professor `P01` e código do curso `C01`.
5. Escolha `5. Relatório integrado` e confira a frase gerada.
6. Feche e execute novamente para confirmar que os dados persistem.

## Observações
- A interface principal é por console para facilitar o teste de todos os requisitos de CRUD e dos relacionamentos em uma única entrada. As interfaces gráficas originais das equipes foram preservadas nas pastas `alfa/` e `beta/`.
- Não apague os arquivos TXT enquanto o programa estiver aberto.
- Os arquivos de dados devem conter um registro por linha e campos separados por ponto e vírgula. Evite usar `;` dentro dos próprios campos.


## 6. Módulo de Avaliação Acadêmica — RF19 a RF24

- **RF19:** A entidade `Avaliacao` possui matrícula, código da disciplina, três notas e três pesos. Os vínculos com aluno e disciplina são verificados.
- **RF20:** O arquivo `dados/notas.txt` utiliza `matricula;codigo_disciplina;nota1;peso1;nota2;peso2;nota3;peso3`.
- **RF21:** A média é calculada em tempo de execução: `sum(nota × peso) / sum(pesos)`.
- **RF22:** Notas de 0 a 10, pesos não negativos e soma de pesos maior que zero. A média é limitada a 10.
- **RF23:** O relatório apresenta aluno, disciplina, notas, pesos, média e status (aprovado com média >= 7).
- **RF24:** `listar()` relê `notas.txt` em cada consulta, recalculando a média após mudanças no arquivo.

### Teste
1. Cadastre um curso, professor, aluno e disciplina vinculados nos menus 1 a 4.
2. Selecione `6. Avaliações e Notas` e cadastre notas 8.5 (peso 2), 7 (peso 3), 9 (peso 5).
3. A média será 8.30, com status Aprovado.
4. Altere uma nota pelo menu 3 ou diretamente no TXT e consulte novamente o relatório.
5. Notas acima de 10, pesos negativos e somatório zero são rejeitados.
