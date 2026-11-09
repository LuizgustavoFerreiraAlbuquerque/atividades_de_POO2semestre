from dataclasses import dataclass

@dataclass
class Avaliacao:
    matricula: str
    codigo_disciplina: str
    nota1: float
    peso1: float
    nota2: float
    peso2: float
    nota3: float
    peso3: float

    @property
    def media(self):
        pesos = self.peso1 + self.peso2 + self.peso3
        if pesos <= 0:
            raise ValueError("A soma dos pesos deve ser maior que zero.")
        return min(10.0, (self.nota1*self.peso1 + self.nota2*self.peso2 + self.nota3*self.peso3) / pesos)

    @property
    def status(self):
        return "Aprovado" if self.media >= 7 else "Reprovado"
