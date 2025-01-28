class TransacaoBancaria:
    def __init__(self):
        # Inicializa um log para registrar todas as transações realizadas.
        self.log = []

    def transferir(self, conta_origem, conta_destino, valor):
        """
        Realiza uma transferência de um valor entre duas contas bancárias, garantindo
        segurança com o uso de locks para evitar condições de corrida.
        
        Parâmetros:
        - conta_origem: ContaBancaria, conta que envia o dinheiro.
        - conta_destino: ContaBancaria, conta que recebe o dinheiro.
        - valor: float, valor a ser transferido.
        """
        # Determina a ordem de bloqueio para evitar deadlocks.
        # Sempre bloqueia primeiro a conta com menor ID.
        primeira, segunda = (
            (conta_origem, conta_destino)
            if conta_origem.id_conta < conta_destino.id_conta
            else (conta_destino, conta_origem)
        )

        # Adquire o lock da primeira conta.
        with primeira.lock:
            # Adquire o lock da segunda conta.
            with segunda.lock:
                # Verifica se a conta de origem possui saldo suficiente.
                if conta_origem.saldo >= valor:
                    # Deduz o valor do saldo da conta de origem.
                    conta_origem.saldo -= valor
                    # Adiciona o valor ao saldo da conta de destino.
                    conta_destino.saldo += valor
                    # Registra a transferência no log.
                    self.log.append(
                        f"Transferência de {valor:.2f} de Conta {conta_origem.id_conta} para Conta {conta_destino.id_conta}"
                    )
                    # Imprime uma mensagem de sucesso.
                    print(f"Transferência de {valor:.2f} realizada com sucesso!")
                else:
                    # Caso não haja saldo suficiente, registra a falha no log.
                    self.log.append(
                        f"Falha: Saldo insuficiente na Conta {conta_origem.id_conta}"
                    )
                    # Imprime uma mensagem indicando saldo insuficiente.
                    print("Saldo insuficiente para a transferência.")
