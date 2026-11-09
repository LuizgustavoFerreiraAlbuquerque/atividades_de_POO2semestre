from dataclasses import dataclass

@dataclass
class Aluno:
    matricula: str
    nome: str
    cpf: str
    email: str
    codigo_curso: str

@dataclass
class Curso:
    codigo: str
    nome: str
    modalidade: str

@dataclass
class Professor:
    codigo: str
    nome: str
    cpf: str
    especialidade: str

@dataclass
class Disciplina:
    codigo: str
    nome: str
    carga_horaria: int
    codigo_professor: str
    codigo_curso: str
