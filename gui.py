import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from gestor_de_tarefas import GestorDeTarefas

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Tarefas")
        self.gestor = GestorDeTarefas()

        # Frame para adicionar tarefa
        self.frame_adicionar = tk.Frame(self.root)
        self.frame_adicionar.pack(pady=10)

        self.label_descricao = tk.Label(self.frame_adicionar, text="Descrição:")
        self.label_descricao.grid(row=0, column=0)
        self.entry_descricao = tk.Entry(self.frame_adicionar, width=30)
        self.entry_descricao.grid(row=0, column=1)

        self.label_prioridade = tk.Label(self.frame_adicionar, text="Prioridade:")
        self.label_prioridade.grid(row=1, column=0)
        self.prioridade_var = tk.StringVar()
        self.combo_prioridade = ttk.Combobox(self.frame_adicionar,
                                             textvariable=self.prioridade_var,
                                             values=["1", "2", "3"],
                                             state="readonly",
                                             width=5)
        self.combo_prioridade.set("1")  # valor padrão
        self.combo_prioridade.grid(row=1, column=1)

        self.button_adicionar = tk.Button(self.frame_adicionar, text="Adicionar Tarefa", command=self.adicionar_tarefa)
        self.button_adicionar.grid(row=2, columnspan=2, pady=5)

        # Frame para listar tarefas
        self.frame_listar = tk.Frame(self.root)
        self.frame_listar.pack(pady=10, fill=tk.BOTH, expand=True)

        self.button_listar = tk.Button(self.frame_listar, text="Atualizar Lista", command=self.listar_tarefas)
        self.button_listar.pack()

        self.text_tarefas = tk.Text(self.frame_listar, width=50, height=10)
        self.text_tarefas.pack(fill=tk.BOTH, expand=True)

        # Frame para operações adicionais
        self.frame_operacoes = tk.Frame(self.root)
        self.frame_operacoes.pack(pady=10)

        self.button_editar = tk.Button(self.frame_operacoes, text="Editar Tarefa", command=self.editar_tarefa)
        self.button_editar.grid(row=0, column=0, padx=5)

        self.button_concluir = tk.Button(self.frame_operacoes, text="Concluir Tarefa", command=self.concluir_tarefa)
        self.button_concluir.grid(row=0, column=1, padx=5)

        self.button_apagar = tk.Button(self.frame_operacoes, text="Apagar Tarefa", command=self.apagar_tarefa)
        self.button_apagar.grid(row=0, column=2, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.listar_tarefas()

    def adicionar_tarefa(self):
        descricao = self.entry_descricao.get()
        prioridade = int(self.prioridade_var.get())
        self.gestor.adicionar_tarefa(descricao, prioridade)
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
        self.entry_descricao.delete(0, tk.END)
        self.combo_prioridade.set("1")
        self.listar_tarefas()

    def listar_tarefas(self):
        self.text_tarefas.delete('1.0', tk.END)
        tarefas = self.gestor.listar_tarefas()
        if not tarefas:
            self.text_tarefas.insert(tk.END, "Nenhuma tarefa encontrada.")
        else:
            for idx, tarefa in enumerate(tarefas, start=1):
                self.text_tarefas.insert(tk.END, f"{idx}. {tarefa}\n")

    def selecionar_tarefa(self, operacao):
        """Abre uma janela para o usuário selecionar uma tarefa existente.
           Retorna o índice da tarefa selecionada ou None se não houver tarefas."""
        tarefas = self.gestor.listar_tarefas()
        if not tarefas:
            messagebox.showinfo("Info", "Nenhuma tarefa disponível.")
            return None

        top = tk.Toplevel(self.root)
        top.title(f"Selecionar tarefa para {operacao}")

        label = tk.Label(top, text="Selecione uma tarefa:")
        label.pack(pady=5)

        combobox = ttk.Combobox(top, values=tarefas, state="readonly", width=50)
        combobox.pack(pady=5)
        combobox.current(0)

        # Variável para guardar o índice selecionado
        selecionado = {'index': None}

        def confirmar():
            selecionado['index'] = combobox.current()
            top.destroy()

        button_confirma = tk.Button(top, text="Confirmar", command=confirmar)
        button_confirma.pack(pady=5)

        top.grab_set()  # Torna a janela modal
        top.wait_window()
        return selecionado['index']

    def editar_tarefa(self):
        indice = self.selecionar_tarefa("edição")
        if indice is not None:
            nova_descricao = simpledialog.askstring("Editar Tarefa", "Digite a nova descrição:")
            if nova_descricao:
                self.gestor.editar_tarefa(indice, nova_descricao)
                self.listar_tarefas()
            else:
                messagebox.showinfo("Info", "Nenhuma alteração efetuada.")

    def concluir_tarefa(self):
        indice = self.selecionar_tarefa("conclusão")
        if indice is not None:
            self.gestor.marcar_concluida(indice)
            self.listar_tarefas()

    def apagar_tarefa(self):
        indice = self.selecionar_tarefa("remoção")
        if indice is not None:
            self.gestor.apagar_tarefa(indice)
            self.listar_tarefas()

    def on_closing(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

