import threading

class ContaBancaria:
    def __init__(self, id_conta, saldo):
        self.id_conta = id_conta
        self.saldo = saldo
        self.lock = threading.Lock()

    def __str__(self):
        return f"Conta {self.id_conta} - Saldo: {self.saldo:.2f}"
