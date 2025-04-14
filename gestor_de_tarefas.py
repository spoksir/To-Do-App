
import json
from tarefa import Tarefa

class GestorDeTarefas:
    def __init__(self):
        self.tarefas = []
        self.carregar_tarefas()

    def adicionar_tarefa(self, descricao, prioridade):
        if not descricao.strip():
            raise ValueError("Descrição não pode estar vazia")
        if prioridade not in [1, 2, 3]:
            raise ValueError("Prioridade deve ser 1, 2 ou 3")
        nova_tarefa = Tarefa(descricao, prioridade)
        self.tarefas.append(nova_tarefa)
        self.salvar_tarefas()

    def listar_tarefas(self):
        if not self.tarefas:
            return []
        return [str(tarefa) for tarefa in self.tarefas]

    def editar_tarefa(self, indice, nova_descricao):
        if not nova_descricao.strip():
            raise ValueError("Nova descrição não pode estar vazia")
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice].descricao = nova_descricao.strip()
            self.salvar_tarefas()
        else:
            raise IndexError("Índice inválido")

    def marcar_concluida(self, indice):
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice].concluir()
            self.salvar_tarefas()
        else:
            raise IndexError("Índice inválido")

    def apagar_tarefa(self, indice):
        if 0 <= indice < len(self.tarefas):
            self.tarefas.pop(indice)
            self.salvar_tarefas()
        else:
            raise IndexError("Índice inválido")

    def ordenar_por_status(self, status_desejado):
        """
        Filtra tarefas por status
        :param status_desejado: bool, True para concluídas, False para pendentes
        :return: list of str
        """
        tarefas_filtradas = [tarefa for tarefa in self.tarefas if tarefa.status == status_desejado]
        if not tarefas_filtradas:
            return []
        return [str(tarefa) for tarefa in tarefas_filtradas]

    def ordenar_por_prioridade(self, prioridade_desejada):
        """
        Filtra tarefas por prioridade
        :param prioridade_desejada: int, 1 (Alta), 2 (Média) ou 3 (Baixa)
        :return: list of str
        """
        if prioridade_desejada not in [1, 2, 3]:
            raise ValueError("Prioridade deve ser 1, 2 ou 3")
        tarefas_filtradas = [tarefa for tarefa in self.tarefas if tarefa.prioridade == prioridade_desejada]
        if not tarefas_filtradas:
            return []
        return [str(tarefa) for tarefa in tarefas_filtradas]

    def salvar_tarefas(self):
        """Salva as tarefas em um arquivo JSON"""
        dados = [tarefa.to_dict() for tarefa in self.tarefas]
        try:
            with open('tarefas.json', 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar tarefas: {e}")

    def carregar_tarefas(self):
        """Carrega as tarefas do arquivo JSON"""
        try:
            with open('tarefas.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                self.tarefas = [Tarefa.from_dict(dado) for dado in dados]
        except FileNotFoundError:
            self.tarefas = []  # Arquivo não existe ainda
        except Exception as e:
            print(f"Erro ao carregar tarefas: {e}")
            self.tarefas = []
