import threading # para utilizar o recurso de locks(travas)

class ContaBancaria:
    def __init__(self, id_conta, saldo):
        self.id_conta = id_conta  # Identificador único para a conta bancária
        self.saldo = saldo  # Saldo inicial da conta
        self.lock = threading.Lock()  # Lock (trava) para garantir exclusividade no acesso ao saldo

    def __str__(self):
        return f"Conta {self.id_conta} - Saldo: {self.saldo:.2f}"  # Representação em string da conta bancária
