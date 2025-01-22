class TransacaoBancaria:
    def __init__(self):
        self.log = []

    def transferir(self, conta_origem, conta_destino, valor):
        primeira, segunda = (conta_origem, conta_destino) if conta_origem.id_conta < conta_destino.id_conta else (conta_destino, conta_origem)

        with primeira.lock:
            with segunda.lock:
                if conta_origem.saldo >= valor:
                    conta_origem.saldo -= valor
                    conta_destino.saldo += valor
                    self.log.append(f"Transferência de {valor:.2f} de Conta {conta_origem.id_conta} para Conta {conta_destino.id_conta}")
                    print(f"Transferência de {valor:.2f} realizada com sucesso!")
                else:
                    self.log.append(f"Falha: Saldo insuficiente na Conta {conta_origem.id_conta}")
                    print("Saldo insuficiente para a transferência.")
