from abc import ABC, abstractmethod
from datetime import datetime

class Tarefa:
    def __init__(self, descricao, prioridade):
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = False
        self.data_criacao = datetime.now()

    def __str__(self):
        status = "Concluída" if self.status else "Pendente"
        return f"{self.descricao} (Prioridade: {self.prioridade}, Status: {status})"

    def concluir(self):
        self.status = True

    def to_dict(self):
        return {
            'descricao': self.descricao,
            'prioridade': self.prioridade,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        tarefa = cls(data['descricao'], data['prioridade'])
        tarefa.status = data['status']
        tarefa.data_criacao = datetime.fromisoformat(data['data_criacao'])
        return tarefa

class TarefaBase(ABC):  # Resposta 1a - Classe base abstrata para polimorfismo
    def __init__(self, descricao, prioridade):
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = False
        self.data_limite = None

    @abstractmethod
    def calcular_urgencia(self):  # Resposta 1a - Método polimórfico
        pass

    @abstractmethod
    def formatar_descricao(self):  # Resposta 1a - Método polimórfico
        pass


class TarefaPadrao(TarefaBase):  # Resposta 1a - Implementação concreta
    def calcular_urgencia(self):
        return self.prioridade

    def formatar_descricao(self):
        return f"Tarefa: {self.descricao}"


class TarefaPrazo(TarefaBase):  # Resposta 1a - Implementação concreta
    def __init__(self, descricao, prioridade, data_limite):
        super().__init__(descricao, prioridade)
        self.data_limite = data_limite

    def calcular_urgencia(self):
        if not self.data_limite:
            return self.prioridade

        dias_ate_prazo = (self.data_limite - datetime.now()).days
        if dias_ate_prazo < 0:
            return 1  # Máxima urgência
        elif dias_ate_prazo < 3:
            return min(self.prioridade, 2)
        return self.prioridade

    def formatar_descricao(self):
        prazo = self.data_limite.strftime('%d/%m/%Y') if self.data_limite else "Sem prazo"
        return f"Tarefa com prazo: {self.descricao} (Até: {prazo})"


class TarefaRecorrente(TarefaBase):  # Resposta 1c - Nova implementação polimórfica
    def __init__(self, descricao, prioridade, intervalo_dias):
        super().__init__(descricao, prioridade)
        self.intervalo_dias = intervalo_dias
        self.ultima_conclusao = None

    def calcular_urgencia(self):
        if not self.ultima_conclusao:
            return self.prioridade

        dias_desde_ultima = (datetime.now() - self.ultima_conclusao).days
        if dias_desde_ultima >= self.intervalo_dias:
            return 1  # Máxima urgência
        return self.prioridade

    def formatar_descricao(self):
        return f"Tarefa recorrente: {self.descricao} (A cada {self.intervalo_dias} dias)"

    def concluir(self):
        self.ultima_conclusao = datetime.now()
        self.status = False  # Reativa para próxima recorrência
