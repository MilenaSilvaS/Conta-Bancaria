from TransacaoBancaria import TransacaoBancaria
from ContaBancaria import ContaBancaria  # Importa a classe que representa uma conta bancária.
import threading  # Importa o módulo para trabalhar com threads.
import random  # Importa o módulo para gerar valores aleatórios.

# Lock global para sincronizar impressões no console, evitando que múltiplas threads causem sobreposição.
print_lock = threading.Lock()

# Exibe a lista de contas bancárias disponíveis.
def mostrar_contas(contas):
    print("\nContas disponíveis:")
    for conta in contas:
        print(f"ID: {conta.id_conta}, Saldo: {conta.saldo:.2f}")

# Permite o cadastro de uma nova conta bancária, solicitando um saldo inicial ao usuário.
def cadastrar_conta(contas):
    id_conta = len(contas) + 1  # Define o ID da nova conta como o próximo número disponível.
    saldo = float(input(f"Digite o saldo inicial para a Conta {id_conta}: "))  # Solicita o saldo inicial.
    nova_conta = ContaBancaria(id_conta=id_conta, saldo=saldo)  # Cria uma nova conta bancária.
    contas.append(nova_conta)  # Adiciona a conta à lista de contas.
    print(f"Conta {id_conta} cadastrada com sucesso!\n")

# Realiza transferências aleatórias entre contas, simulando operações concorrentes.
def realizar_transferencias_aleatorias(contas, transacao_bancaria):
    for _ in range(100):  # Cada thread realiza 100 transferências.
        conta_origem = random.choice(contas)  # Seleciona uma conta de origem aleatoriamente.
        conta_destino = random.choice([c for c in contas if c != conta_origem])  # Seleciona uma conta de destino diferente.
        valor = random.uniform(1, 50)  # Define um valor aleatório para a transferência.
        with print_lock:  # Garante que apenas uma thread por vez imprime no console.
            transacao_bancaria.transferir(conta_origem, conta_destino, valor)
            print(f"Transferência de {valor:.2f} realizada com sucesso! Conta origem: {conta_origem.id_conta}, Conta destino: {conta_destino.id_conta}")

# Executa um teste de alta concorrência com múltiplas threads.
def teste_alta_concorrencia(contas, transacao_bancaria):
    print("\nExecutando Cenário 2: Alta Concorrência")
    if len(contas) < 100:
        print("Criando automaticamente 100 contas para o teste...")
        for i in range(100):
            contas.append(ContaBancaria(id_conta=len(contas) + 1, saldo=random.randint(100, 1000)))

    threads = []
    for _ in range(50):  # Cria 50 threads para simular transferências simultâneas.
        thread = threading.Thread(target=realizar_transferencias_aleatorias, args=(contas, transacao_bancaria))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Aguarda a conclusão de todas as threads.

    saldo_total = sum(conta.saldo for conta in contas)  # Calcula o saldo total após o teste.
    print(f"Saldo total após o teste de alta concorrência: {saldo_total}")

# Testa o comportamento do sistema quando há saldo insuficiente para realizar uma transferência.
def teste_saldo_insuficiente(contas, transacao_bancaria):
    print("\nExecutando Cenário 3: Saldo Insuficiente")
    if len(contas) < 2:
        print("Criando automaticamente 2 contas para o teste...")
        contas.append(ContaBancaria(id_conta=len(contas) + 1, saldo=100))
        contas.append(ContaBancaria(id_conta=len(contas) + 1, saldo=200))

    conta_origem = contas[0]
    conta_destino = contas[1]
    valor = conta_origem.saldo + 100  # Define um valor maior que o saldo disponível na conta de origem.
    with print_lock:  # Garante que a mensagem de erro não seja interrompida por outra thread.
        transacao_bancaria.transferir(conta_origem, conta_destino, valor)
        print(f"Transferência de {valor:.2f} falhou! Saldo insuficiente na Conta origem: {conta_origem.id_conta}")
    mostrar_contas(contas)

# Menu principal do sistema.
def main():
    contas = []  # Lista de contas bancárias.
    transacao_bancaria = TransacaoBancaria()  # Instância para gerenciar as transferências.

    while True:
        print("\nMenu do Sistema Bancário")
        print("1. Cadastrar Conta")
        print("2. Mostrar Contas")
        print("3. Realizar Transferência")
        print("4. Executar Cenário 2 (Alta Concorrência)")
        print("5. Executar Cenário 3 (Saldo Insuficiente)")
        print("6. Mostrar Logs")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_conta(contas)
        elif opcao == "2":
            mostrar_contas(contas)
        elif opcao == "3":
            if len(contas) < 2:
                print("É necessário pelo menos 2 contas para realizar transferências.\n")
                continue
            realizar_transferencia(contas, transacao_bancaria)
        elif opcao == "4":
            teste_alta_concorrencia(contas, transacao_bancaria)
        elif opcao == "5":
            teste_saldo_insuficiente(contas, transacao_bancaria)
        elif opcao == "6":
            print("\nLogs de Transações:")
            for log in transacao_bancaria.log:  # Exibe os logs das transferências realizadas.
                print(log)
        elif opcao == "7":
            print("Encerrando o sistema. Até logo!")  # Encerra o sistema.
            break
        else:
            print("Opção inválida. Tente novamente.\n")

# Realiza uma transferência manual entre contas.
def realizar_transferencia(contas, transacao_bancaria):
    try:
        mostrar_contas(contas)
        origem_id = int(input("Digite o ID da conta de origem: "))
        destino_id = int(input("Digite o ID da conta de destino: "))
        valor = float(input("Digite o valor a ser transferido: "))

        conta_origem = next((c for c in contas if c.id_conta == origem_id), None)
        conta_destino = next((c for c in contas if c.id_conta == destino_id), None)

        if not conta_origem or not conta_destino:
            print("Uma ou ambas as contas não existem. Tente novamente.\n")
            return

        with print_lock:
            transacao_bancaria.transferir(conta_origem, conta_destino, valor)
            print(f"Transferência realizada: Conta origem {origem_id} transferiu {valor:.2f} para Conta destino {destino_id}")
    except ValueError:
        print("Entrada inválida. Certifique-se de digitar números válidos.\n")

# Executa o menu principal se o script for executado diretamente.
if __name__ == "__main__":
    main()
