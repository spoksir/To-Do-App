from gestor_de_tarefas import GestorDeTarefas


# Menu
def menu():
    gestor = GestorDeTarefas()

    while True:
        print("\n=== MENU GESTÃO DE TAREFAS ===")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Editar Tarefa")
        print("4. Marcar Tarefa como concluída")
        print("5. Apagar Tarefa")
        print("6. Ordenar Tarefas por Status")
        print("7. Ordenar Tarefas por Prioridade")
        print("8. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            descricao = input("Descrição da tarefa: ")
            print("Prioridade: 1 = Alta, 2 = Média, 3 = Baixa")
            try:
                prioridade = int(input("Escolha a prioridade (1, 2 ou 3): "))
                if prioridade not in [1, 2, 3]:
                    print("Prioridade inválida. Escolha entre 1, 2 ou 3.")
                else:
                    gestor.adicionar_tarefa(descricao, prioridade)
                    print("Tarefa adicionada com sucesso!")
            except ValueError:
                print("Prioridade deve ser um número.")
        elif opcao == "2":
            print("\n=== LISTA DE TAREFAS ===")
            gestor.listar_tarefas()
        elif opcao == "3":
            try:
                gestor.listar_tarefas()
                indice = int(input("Número da tarefa para editar: ")) - 1
                nova_descricao = input("Nova descrição: ")
                gestor.editar_tarefa(indice, nova_descricao)
                print("Tarefa editada com sucesso!")
            except ValueError:
                print("Entrada inválida. Certifique-se de digitar um número.")
        elif opcao == "4":
            try:
                gestor.listar_tarefas()
                indice = int(input("Número da tarefa para marcar como concluída: ")) - 1
                gestor.marcar_concluida(indice)
                print("Tarefa marcada como concluída!")
            except ValueError:
                print("Entrada inválida. Certifique-se de digitar um número.")
        elif opcao == "5":
            try:
                gestor.listar_tarefas()
                indice = int(input("Número da tarefa para apagar: ")) - 1
                gestor.apagar_tarefa(indice)
                print("Tarefa apagada com sucesso!")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        elif opcao == "6":
            print("1. Pendentes\n2. Concluídas")
            try:
                status = int(input("Escolha o status (1 para Pendentes, 2 para Concluídas): "))
                if status == 1:
                    gestor.ordenar_por_status(False)
                elif status == 2:
                    gestor.ordenar_por_status(True)
                else:
                    print("Opção inválida. Escolha 1 ou 2.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        elif opcao == "7":
            print("Prioridade: 1 = Alta, 2 = Média, 3 = Baixa")
            try:
                prioridade = int(input("Escolha a prioridade (1, 2 ou 3): "))
                if prioridade in [1, 2, 3]:
                    gestor.ordenar_por_prioridade(prioridade)
                else:
                    print("Prioridade inválida. Escolha entre 1, 2 ou 3.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        elif opcao == "8":
            print("A encerrar o programa. Obrigado!")
            break
        else:
            print("Opção inválida. Tente novamente.")
