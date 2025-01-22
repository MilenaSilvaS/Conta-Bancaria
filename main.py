from TransacaoBancaria import TransacaoBancaria
from ContaBancaria import ContaBancaria
import threading
import random

# Lock global para sincronizar impressões
print_lock = threading.Lock()

def mostrar_contas(contas):
    print("\nContas disponíveis:")
    for conta in contas:
        print(f"ID: {conta.id_conta}, Saldo: {conta.saldo:.2f}")

def cadastrar_conta(contas):
    id_conta = len(contas) + 1
    saldo = float(input(f"Digite o saldo inicial para a Conta {id_conta}: "))
    nova_conta = ContaBancaria(id_conta=id_conta, saldo=saldo)
    contas.append(nova_conta)
    print(f"Conta {id_conta} cadastrada com sucesso!\n")

def realizar_transferencias_aleatorias(contas, transacao_bancaria):
    for _ in range(100):  # Cada thread realiza 100 transferências
        conta_origem = random.choice(contas)
        conta_destino = random.choice([c for c in contas if c != conta_origem])
        valor = random.uniform(1, 50)
        with print_lock:
            transacao_bancaria.transferir(conta_origem, conta_destino, valor)
            print(f"Transferência de {valor:.2f} realizada com sucesso! Conta origem: {conta_origem.id_conta}, Conta destino: {conta_destino.id_conta}")

def teste_alta_concorrencia(contas, transacao_bancaria):
    print("\nExecutando Cenário 2: Alta Concorrência")
    if len(contas) < 100:
        print("Criando automaticamente 100 contas para o teste...")
        for i in range(100):
            contas.append(ContaBancaria(id_conta=len(contas) + 1, saldo=random.randint(100, 1000)))

    threads = []
    for _ in range(50):  # 50 threads
        thread = threading.Thread(target=realizar_transferencias_aleatorias, args=(contas, transacao_bancaria))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    saldo_total = sum(conta.saldo for conta in contas)
    print(f"Saldo total após o teste de alta concorrência: {saldo_total}")

def teste_saldo_insuficiente(contas, transacao_bancaria):
    print("\nExecutando Cenário 3: Saldo Insuficiente")
    if len(contas) < 2:
        print("Criando automaticamente 2 contas para o teste...")
        contas.append(ContaBancaria(id_conta=len(contas) + 1, saldo=100))
        contas.append(ContaBancaria(id_conta=len(contas) + 1, saldo=200))

    conta_origem = contas[0]
    conta_destino = contas[1]
    valor = conta_origem.saldo + 100  # Valor superior ao saldo disponível
    with print_lock:
        transacao_bancaria.transferir(conta_origem, conta_destino, valor)
        print(f"Transferência de {valor:.2f} falhou! Saldo insuficiente na Conta origem: {conta_origem.id_conta}")
    mostrar_contas(contas)

def main():
    contas = []
    transacao_bancaria = TransacaoBancaria()

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
            for log in transacao_bancaria.log:
                print(log)
        elif opcao == "7":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

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

if __name__ == "__main__":
    main()
